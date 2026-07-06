#!/usr/bin/env python3
"""ETA gauge for the opinions COPY: read the bzcat process's actual bytes-read from /proc/PID/io
and compare to the .bz2 file size."""
import os, glob, time

TOT = "/archive/courtlistener/bulk/opinions-2026-06-30.csv.bz2"
tot = os.path.getsize(TOT)
pid = None
for p in glob.glob("/proc/[0-9]*/cmdline"):
    try:
        cl = open(p, "rb").read().replace(b"\x00", b" ").decode("utf-8", "replace")
    except Exception:
        continue
    if cl.strip().startswith("bzcat") and "opinions-2026-06-30" in cl:  # the real bzcat, not sh -c
        pid = p.split("/")[2]
        break
if not pid:
    print("no bzcat running (COPY may be committing, or in the CTAS/lean phase, or done)")
    raise SystemExit


def readbytes(pid):
    for ln in open("/proc/%s/io" % pid):
        if ln.startswith("rchar:"):   # chars read incl. page cache (read_bytes=0 when file is cached)
            return int(ln.split()[1])
    return 0


b0 = readbytes(pid)
time.sleep(20)
b1 = readbytes(pid)
rate = (b1 - b0) / 20.0  # bytes/sec of compressed input consumed
pct = 100 * b1 / tot
remain = (tot - b1) / rate / 60 if rate > 0 else float("inf")
print("bzcat read %.1f%% (%.1f/%.1f GB compressed), rate %.1f MB/s compressed, ETA ~%.0f min"
      % (pct, b1 / 1e9, tot / 1e9, rate / 1e6, remain))
