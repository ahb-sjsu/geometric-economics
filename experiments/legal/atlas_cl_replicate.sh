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
FILES=(courts dockets originating-court-information opinion-clusters opinions citation-map \
       people-db-people people-db-positions)

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

load() {
  command -v psql >/dev/null || { echo "psql not found"; exit 1; }
  tablespace
  $PG -tc "SELECT 1 FROM pg_database WHERE datname='$DB'" | grep -q 1 \
    || sudo -u postgres createdb "$DB" -D "$TS"
  echo "[load] schema -> $DB (tablespace $TS)"
  $PG -d "$DB" -f "$BULK/schema-$DUMP.sql"
  # COPY each bz2 straight into its table via bzcat. Superuser (postgres) can COPY FROM PROGRAM;
  # bulk files are world-readable so the postgres OS user can bzcat them.
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
  for f in "${FILES[@]}"; do
    tbl="${TBL[$f]}"
    echo "[load] COPY $f -> $tbl ($(date))"
    $PG -d "$DB" -c "COPY $tbl FROM PROGRAM 'bzcat $BULK/$f-$DUMP.csv.bz2' WITH (FORMAT csv, HEADER true);"
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
