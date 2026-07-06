#!/usr/bin/env python3
"""Stage 3 (POST-FREEZE, prereg-legal-reversal-v1): build district->circuit reversal labels on the
Atlas CourtListener replica.

Links each U.S. District Court merits opinion (jurisdiction FD, filed 1990-2015) to its reviewing
U.S. Court of Appeals opinion via authoritative docket lineage
(search_docket.originating_court_information_id -> originating docket_number == the district docket
number), parses the circuit opinion's disposition (reverse/vacate vs affirm) and the ground->deontic
gate, and writes a reversal_labels table with the temporal split.

Runs ON ATLAS. This is post-freeze: the freeze tag prereg-legal-reversal-v1 is an ancestor of this.

    python3 cl_build_labels.py --counts   # validate feasibility + label distribution first
    python3 cl_build_labels.py --build    # create reversal_labels table
"""
import argparse, subprocess, sys

def psql(sql, timeout=1800, tuples=False):
    args = ["sudo", "-u", "postgres", "psql", "-d", "courtlistener", "-v", "ON_ERROR_STOP=1"]
    if tuples:
        args += ["-tAF", "\t"]
    args += ["-c", sql]
    r = subprocess.run(args, capture_output=True, text=True, timeout=timeout)
    if r.returncode != 0:
        raise RuntimeError(r.stderr.strip()[:600])
    return r.stdout

# the reviewed-pair CTE: district merits opinion -> its reviewing circuit opinion (authoritative lineage)
PAIRS_CTE = r"""
WITH pairs AS (
  SELECT
    dop.id            AS district_opinion_id,
    dc.date_filed     AS district_date,
    dd.court_id       AS district_court,
    cop.id            AS circuit_opinion_id,
    coalesce(nullif(cop.plain_text,''), cop.html_with_citations) AS circuit_text
  FROM search_opinioncluster dc
  JOIN search_docket dd            ON dd.id = dc.docket_id
  JOIN search_court dcourt         ON dcourt.id = dd.court_id AND dcourt.jurisdiction = 'FD'
  JOIN search_opinion dop          ON dop.cluster_id = dc.id
  JOIN search_originatingcourtinformation oci ON oci.docket_number = dd.docket_number AND oci.docket_number <> ''
  JOIN search_docket cd            ON cd.originating_court_information_id = oci.id
  JOIN search_court ccourt         ON ccourt.id = cd.court_id AND ccourt.jurisdiction = 'F'
  JOIN search_opinioncluster cc    ON cc.docket_id = cd.id
  JOIN search_opinion cop          ON cop.cluster_id = cc.id
  WHERE dc.date_filed BETWEEN '1990-01-01' AND '2015-12-31'
)
"""

DISP = "(circuit_text ~* '\\y(revers|vacat)' )"      # crude first-pass; KeyCite-validated per prereg
AFF  = "(circuit_text ~* '\\yaffirm')"


def counts():
    print("== Stage 3 label feasibility/distribution (post-freeze) ==")
    print("district FD merits opinions 1990-2015:")
    print(psql("SELECT count(*) FROM search_opinioncluster dc "
               "JOIN search_docket dd ON dd.id=dc.docket_id "
               "JOIN search_court c ON c.id=dd.court_id AND c.jurisdiction='FD' "
               "JOIN search_opinion o ON o.cluster_id=dc.id "
               "WHERE dc.date_filed BETWEEN '1990-01-01' AND '2015-12-31';", tuples=True).strip())
    print("\nreviewed pairs (district decision linked to a circuit reviewer) + disposition split:")
    print(psql(PAIRS_CTE +
               f"SELECT count(*) AS pairs, "
               f"sum(({DISP})::int) AS reverse_ish, sum(({AFF})::int) AS affirm_ish, "
               f"sum((NOT {DISP} AND NOT {AFF})::int) AS unclear FROM pairs;", tuples=True).strip())


def build():
    print("== Stage 3 build reversal_labels (post-freeze) ==")
    psql("DROP TABLE IF EXISTS reversal_labels;")
    psql(PAIRS_CTE + f"""
    , labeled AS (
      SELECT district_opinion_id, district_date, district_court, circuit_opinion_id,
        CASE WHEN {DISP} THEN 1 WHEN {AFF} THEN 0 ELSE NULL END AS reversed,
        (circuit_text ~* 'jurisdic|standing|ultra vires|lacked (the )?authority') AS g_authority,
        (circuit_text ~* 'due process|waiver|voluntar|coerc|without consent')      AS g_consent,
        (circuit_text ~* 'equal protection|similarly situated|disparate treatment') AS g_universal,
        (circuit_text ~* 'cruel and unusual|human dignity|instrumentaliz')          AS g_mere_means,
        CASE WHEN district_date < '2008-01-01' THEN 'train'
             WHEN district_date < '2012-01-01' THEN 'val' ELSE 'test' END AS split
      FROM pairs
    )
    SELECT DISTINCT ON (district_opinion_id) * INTO reversal_labels FROM labeled
    WHERE reversed IS NOT NULL;""")
    psql("CREATE INDEX ix_rl_opinion ON reversal_labels (district_opinion_id);")
    print(psql("SELECT split, count(*) AS n, sum(reversed) AS reversed, "
               "round(avg(reversed)::numeric,3) AS reverse_rate, "
               "sum((g_authority OR g_consent OR g_universal OR g_mere_means)::int) AS gate_aligned "
               "FROM reversal_labels GROUP BY split ORDER BY split;", tuples=True))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--counts", action="store_true")
    ap.add_argument("--build", action="store_true")
    a = ap.parse_args()
    if a.counts: counts()
    elif a.build: build()
    else: print("use --counts then --build")


if __name__ == "__main__":
    main()
