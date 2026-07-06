#!/usr/bin/env python3
"""Work out the docket-number normalization regex so district dockets match the circuit's recorded
originating docket. Federal district numbers look like '1:23-cv-02699-ABC' (office : YY - type -
seq - judge). Canonical key = YY-type-seq with office prefix, judge suffix, and leading zeros dropped.
Shows samples of both sides' normalized keys and counts how many pairs match. Runs ON ATLAS."""
import subprocess

# Postgres: canonical key = last-2-digit year + case type + seq (leading zeros dropped). Century
# optional so '2013-cv' and '13-cv' both -> '13'. NULL if no match.
NORM = (r"array_to_string(regexp_match(lower({c}), "
        r"'(?:19|20)?(\d{{2}})[-: ]?(cv|cr|cvb|md|mc|mj|bk|adv|civ)[- .]*0*(\d+)'), '-')")


def psql(sql, timeout=600):
    r = subprocess.run(["sudo", "-u", "postgres", "psql", "-d", "courtlistener",
                        "-v", "ON_ERROR_STOP=1", "-tAF", "|", "-c", sql],
                       capture_output=True, text=True, timeout=timeout)
    if r.returncode != 0:
        raise RuntimeError(r.stderr.strip()[:600])
    return r.stdout.strip()


def main():
    print("== district FD docket_number -> normalized key ==")
    print(psql(f"SELECT docket_number, {NORM.format(c='docket_number')} FROM search_docket d "
               f"JOIN search_court c ON c.id=d.court_id AND c.jurisdiction='FD' "
               f"WHERE docket_number ~ '(cv|cr)' LIMIT 8;"))
    print("\n== originating docket_number -> normalized key ==")
    print(psql(f"SELECT docket_number, {NORM.format(c='docket_number')} FROM search_originatingcourtinformation "
               f"WHERE docket_number ~ '(cv|cr)' LIMIT 8;"))

    print("\n== build normalized temp tables + count matched district->circuit pairs ==")
    psql("DROP TABLE IF EXISTS d_norm; DROP TABLE IF EXISTS c_norm;")
    psql(f"""CREATE TABLE d_norm AS
      SELECT dop.id AS district_opinion_id, dc.date_filed AS district_date, dd.court_id AS district_court,
             {NORM.format(c='dd.docket_number')} AS dn
      FROM search_opinioncluster dc
      JOIN search_docket dd ON dd.id=dc.docket_id
      JOIN search_court c ON c.id=dd.court_id AND c.jurisdiction='FD'
      JOIN search_opinion dop ON dop.cluster_id=dc.id
      WHERE dc.date_filed BETWEEN '1990-01-01' AND '2015-12-31';""")
    psql(f"""CREATE TABLE c_norm AS
      SELECT cop.id AS circuit_opinion_id, dd.court_id AS circuit_court,
             {NORM.format(c='oci.docket_number')} AS dn
      FROM search_originatingcourtinformation oci
      JOIN search_docket dd ON dd.originating_court_information_id=oci.id
      JOIN search_court c ON c.id=dd.court_id AND c.jurisdiction='F'
      JOIN search_opinioncluster ccl ON ccl.docket_id=dd.id
      JOIN search_opinion cop ON cop.cluster_id=ccl.id;""")
    psql("CREATE INDEX ix_dnorm ON d_norm(dn); CREATE INDEX ix_cnorm ON c_norm(dn);")
    print("d_norm rows / non-null dn: " + psql("SELECT count(*), count(dn) FROM d_norm;"))
    print("c_norm rows / non-null dn: " + psql("SELECT count(*), count(dn) FROM c_norm;"))
    print("district docket coverage (empty vs non-empty-unparseable): " +
          psql(f"SELECT sum((dd.docket_number='')::int) empty, "
               f"sum((dd.docket_number<>'' AND {NORM.format(c='dd.docket_number')} IS NULL)::int) unparseable "
               f"FROM search_opinioncluster dc JOIN search_docket dd ON dd.id=dc.docket_id "
               f"JOIN search_court c ON c.id=dd.court_id AND c.jurisdiction='FD' "
               f"WHERE dc.date_filed BETWEEN '1990-01-01' AND '2015-12-31';"))
    print("(A) docket-lineage matched pairs: " +
          psql("SELECT count(DISTINCT d.district_opinion_id) FROM d_norm d JOIN c_norm c ON c.dn=d.dn "
               "WHERE d.dn IS NOT NULL AND c.circuit_court <> d.district_court;"))
    # (B) citation-graph linkage: FD district merits opinion cited by a circuit (jurisdiction F) opinion
    print("(B) citation-linkage pairs (district opinion cited by a circuit opinion): " +
          psql("SELECT count(DISTINCT d.district_opinion_id) "
               "FROM d_norm d JOIN search_opinionscited oc ON oc.cited_opinion_id=d.district_opinion_id "
               "JOIN search_opinion co ON co.id=oc.citing_opinion_id "
               "JOIN search_opinioncluster cc ON cc.id=co.cluster_id "
               "JOIN search_docket cd ON cd.id=cc.docket_id "
               "JOIN search_court c ON c.id=cd.court_id AND c.jurisdiction='F';", timeout=1200))


if __name__ == "__main__":
    main()
