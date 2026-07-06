#!/usr/bin/env bash
# Fast NATIVE load of opinions: Postgres COPY (no Python) into an all-text raw table using
# ESCAPE '\' (validated: parses the CourtListener backslash-quote/CR format), then cast into the
# lean typed search_opinion (10 cols; drop the 6 redundant html/xml renderings). ~1 hr vs ~9 hr.
#
# opinions CSV cols (0-based): 0 id,1 date_created,2 date_modified,3 author_str,4 per_curiam,
# 5 joined_by_str,6 type,7 sha1,8 page_count,9 download_url,10 local_path,11 plain_text,12 html,
# 13 html_lawbox,14 html_columbia,15 html_anon_2020,16 xml_harvard,17 xml_scan,18 html_with_citations,
# 19 extracted_by_ocr,20 author_id,21 cluster_id
set -uo pipefail
DB=courtlistener; PG="sudo -u postgres psql"; BULK=/archive/courtlistener/bulk; DUMP=2026-06-30
F="$BULK/opinions-$DUMP.csv.bz2"

echo "[native] kill any prior opinions load ($(date))"
# match prior-load WORKERS only (not this script's own name -> avoid self-kill); exclude self PID
ps -eo pid,cmd | grep -E "bzcat .*opinions-$DUMP|_cl_normalize|copy search_opinion" \
  | grep -v grep | awk -v me=$$ '$1!=me{print $1}' | xargs -r sudo kill 2>/dev/null || true
sleep 2

echo "[native] raw all-text table + native COPY (ESCAPE backslash) start $(date)"
cols=$(python3 -c "print(','.join('c%d text'%i for i in range(22)))")
$PG -d "$DB" -c "DROP TABLE IF EXISTS search_opinion_raw;"
$PG -d "$DB" -c "CREATE TABLE search_opinion_raw ($cols);"
$PG -d "$DB" -c "COPY search_opinion_raw FROM PROGRAM 'bzcat $F' WITH (FORMAT csv, HEADER true, ESCAPE '\');"
echo -n "[native] raw rows ($(date)): "; $PG -d "$DB" -tc "SELECT count(*) FROM search_opinion_raw;"

echo "[native] build lean typed search_opinion (cast join keys, keep 2 text cols)"
$PG -d "$DB" -c "DROP TABLE IF EXISTS search_opinion;"
$PG -d "$DB" -c "CREATE TABLE search_opinion AS SELECT
  nullif(c0,'')::int      AS id,
  nullif(c4,'')::boolean  AS per_curiam,
  c6                      AS type,
  c7                      AS sha1,
  nullif(c8,'')::int      AS page_count,
  c11                     AS plain_text,
  c18                     AS html_with_citations,
  nullif(c19,'')::boolean AS extracted_by_ocr,
  nullif(c20,'')::int     AS author_id,
  nullif(c21,'')::int     AS cluster_id
FROM search_opinion_raw;"
$PG -d "$DB" -c "DROP TABLE search_opinion_raw;"
echo -n "[native] done ($(date)): "
$PG -d "$DB" -tc "SELECT count(*) AS opinions, pg_size_pretty(pg_total_relation_size('search_opinion')) AS size FROM search_opinion;"
