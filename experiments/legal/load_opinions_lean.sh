#!/usr/bin/env bash
# Reload ONLY the opinions table with a lean column set (kills the in-flight full-column load first;
# the other 7 tables stay loaded). Drops the 6 redundant text renderings (html, html_lawbox,
# html_columbia, html_anon_2020, xml_harvard, xml_scan) + download_url/local_path/dates; keeps
# plain_text (compiler input) + html_with_citations (fallback text) -> ~4-6x faster load.
#
# opinions CSV column order (0-based): 0 id, 1 date_created, 2 date_modified, 3 author_str,
# 4 per_curiam, 5 joined_by_str, 6 type, 7 sha1, 8 page_count, 9 download_url, 10 local_path,
# 11 plain_text, 12 html, 13 html_lawbox, 14 html_columbia, 15 html_anon_2020, 16 xml_harvard,
# 17 xml_scan, 18 html_with_citations, 19 extracted_by_ocr, 20 author_id, 21 cluster_id
set -uo pipefail
ROOT=/archive/courtlistener; BULK=$ROOT/bulk; DUMP=2026-06-30; DB=courtlistener
PG="sudo -u postgres psql"
F="$BULK/opinions-$DUMP.csv.bz2"

echo "[lean] killing in-flight opinions load ($(date))"
ps -eo pid,cmd | grep -E "opinions-$DUMP|_cl_normalize|copy search_opinion|atlas_cl_replicate.sh load" \
  | grep -v grep | awk '{print $1}' | xargs -r sudo kill 2>/dev/null || true
sleep 4

echo "[lean] recreate lean search_opinion"
$PG -d "$DB" -c "DROP TABLE IF EXISTS search_opinion CASCADE;"
$PG -d "$DB" -c "CREATE TABLE search_opinion (id integer, per_curiam boolean, type text, sha1 text, page_count integer, plain_text text, html_with_citations text, extracted_by_ocr boolean, author_id integer, cluster_id integer);"

echo "[lean] COPY opinions (10 cols) start $(date)"
bzcat "$F" | python3 "$ROOT/_cl_normalize_cols.py" 0 4 6 7 8 11 18 19 20 21 | \
  $PG -d "$DB" -c "\copy search_opinion (id,per_curiam,type,sha1,page_count,plain_text,html_with_citations,extracted_by_ocr,author_id,cluster_id) FROM STDIN WITH (FORMAT csv, HEADER true)"
rc=$?
echo "[lean] COPY exit=$rc done $(date)"
$PG -d "$DB" -tc "SELECT count(*) AS opinions, pg_size_pretty(pg_total_relation_size('search_opinion')) AS size FROM search_opinion;"
