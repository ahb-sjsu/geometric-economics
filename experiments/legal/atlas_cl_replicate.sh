#!/usr/bin/env bash
# Replicate the CourtListener bulk case-law database to Atlas /archive and load into a local
# Postgres (data dir on /archive, own port, no system install needed if PG binaries exist).
# Public-domain bulk data (CC Public Domain Mark) -> reproducible, no ToS/ROSS issue.
#
# Removes the API rate-limit/timeout wall: docket lineage, the citation graph, and full text
# become local SQL joins. This is Stage-2/3 INFRASTRUCTURE; the confirmatory pathology<->reversal
# analysis still happens post-freeze (FREEZE_PROTOCOL.md).
#
# Usage on Atlas:
#   bash atlas_cl_replicate.sh download     # Stage A: ~58 GB to /archive (safe, resumable, no sudo)
#   bash atlas_cl_replicate.sh load         # Stage B: initdb in /archive + COPY (needs PG binaries)
#   bash atlas_cl_replicate.sh index        # Stage C: study indexes
set -euo pipefail

DUMP="${CL_DUMP:-2026-06-30}"
ROOT=/archive/courtlistener
BULK="$ROOT/bulk"
PGDATA="$ROOT/pgdata"
PGPORT="${CL_PGPORT:-5433}"          # non-default -> won't touch any existing cluster
DB=courtlistener
BASE=https://storage.courtlistener.com/bulk-data

# tables we need: text, lineage, citation graph, courts, judges (panel IV). Skip embeddings (~2TB).
# order: tiny -> small -> dockets -> opinions LAST (so the 51 GB file's COPY doesn't gate the rest,
# and a mechanic error surfaces on tiny 'courts' in seconds).
FILES=(courts originating-court-information people-db-people people-db-positions \
       citation-map opinion-clusters dockets opinions)

WGET="wget -c --tries=20 --timeout=60 --waitretry=15 --retry-connrefused --progress=dot:giga"
download() {
  mkdir -p "$BULK"; cd "$BULK"
  echo "[download] schema + ${#FILES[@]} tables of dump $DUMP -> $BULK  ($(date))"
  $WGET "$BASE/schema-$DUMP.sql"
  for t in "${FILES[@]}"; do
    echo "  == $t == ($(date))"; $WGET "$BASE/$t-$DUMP.csv.bz2"
  done
  echo "[download] done ($(date))."; du -sh "$BULK"; ls -lh "$BULK"
}

# Use the EXISTING Postgres server (installed) via sudo -u postgres, with a TABLESPACE on /archive
# so the ~0.5 TB of table data lives on the 15 TB disk, not the system disk.
TS=cl_archive
TSDIR="$ROOT/pgts"
PG="sudo -u postgres psql"

tablespace() {
  # tablespace dir must be owned by the postgres OS user and empty
  sudo mkdir -p "$TSDIR"; sudo chown postgres:postgres "$TSDIR"
  $PG -tc "SELECT 1 FROM pg_tablespace WHERE spcname='$TS'" | grep -q 1 \
    || $PG -c "CREATE TABLESPACE $TS LOCATION '$TSDIR';"
}

declare -A TBL=(
  [courts]=search_court
  [dockets]=search_docket
  [originating-court-information]=search_originatingcourtinformation
  [opinion-clusters]=search_opinioncluster
  [opinions]=search_opinion
  [citation-map]=search_opinionscited
  [people-db-people]=people_db_person
  [people-db-positions]=people_db_position
)

load() {
  command -v psql >/dev/null || { echo "psql not found"; exit 1; }
  tablespace
  $PG -tc "SELECT 1 FROM pg_database WHERE datname='$DB'" | grep -q 1 \
    || sudo -u postgres createdb "$DB" -D "$TS"
  # BARE CREATE TABLE (no indexes/FKs -> fast COPY, no FK violations on a partial load) for only
  # the 8 tables we load; extracted from the full pg_dump schema.
  local names=" ${TBL[*]} "
  # strip NOT NULL (bulk CSV writes empty-string NOT-NULL fields as empty -> read as NULL) and inline
  # DEFAULTs (sequences aren't created in the bare subset); read-only research replica, so permissive.
  awk -v names="$names" '
    /^CREATE TABLE public\./ { t=$3; sub(/^public\./,"",t); sub(/\(.*/,"",t); p=(index(names," " t " ")>0) }
    p { print }
    p && /^\);/ { p=0; print "" }
  ' "$BULK/schema-$DUMP.sql" | sed -E 's/ NOT NULL//g; s/ DEFAULT [^,]+//g' > "$ROOT/subset_schema.sql"
  echo "[load] (re)creating bare tables (idempotent)"
  for t in "${TBL[@]}"; do $PG -d "$DB" -c "DROP TABLE IF EXISTS $t CASCADE;" >/dev/null; done
  $PG -d "$DB" -f "$ROOT/subset_schema.sql"
  # COPY via stream: strip \r (embedded \r\n in quoted text fields trips Postgres CSV; harmless for
  # our text features) and pipe to \copy FROM STDIN with a header-derived column list (avoids the
  # FROM PROGRAM quoting mess). Subshell disables pipefail so bzcat|head-1 SIGPIPE doesn't abort.
  for f in "${FILES[@]}"; do
    tbl="${TBL[$f]}"
    hdr=$( set +o pipefail; bzcat "$BULK/$f-$DUMP.csv.bz2" | head -1 | tr -d '\r' )
    echo "[load] COPY $f -> $tbl ($(echo "$hdr" | tr ',' '\n' | wc -l) cols) ($(date))"
    # normalize through Python's CSV parser (Postgres CSV desyncs on these files where Python does not)
    bzcat "$BULK/$f-$DUMP.csv.bz2" | python3 "$ROOT/_cl_normalize.py" | \
      $PG -d "$DB" -c "\copy $tbl ($hdr) FROM STDIN WITH (FORMAT csv, HEADER true)"
  done
  echo "[load] done ($(date))."
}

index() {
  echo "[index] study indexes"
  $PG -d "$DB" <<'SQL'
CREATE INDEX IF NOT EXISTS ix_docket_court_date ON search_docket (court_id, date_filed);
CREATE INDEX IF NOT EXISTS ix_docket_number     ON search_docket (docket_number);
CREATE INDEX IF NOT EXISTS ix_oci_docket        ON search_originatingcourtinformation (docket_number);
CREATE INDEX IF NOT EXISTS ix_cited             ON search_opinionscited (cited_opinion_id);
CREATE INDEX IF NOT EXISTS ix_citing            ON search_opinionscited (citing_opinion_id);
CREATE INDEX IF NOT EXISTS ix_cluster_docket    ON search_opinioncluster (docket_id);
CREATE INDEX IF NOT EXISTS ix_opinion_cluster   ON search_opinion (cluster_id);
SQL
  echo "[index] done. Connect: sudo -u postgres psql -d $DB"
}

case "${1:-}" in
  download) download ;;
  load)     load ;;
  index)    index ;;
  all)      download; load; index ;;
  *) echo "usage: $0 {download|load|index|all}"; exit 2 ;;
esac
