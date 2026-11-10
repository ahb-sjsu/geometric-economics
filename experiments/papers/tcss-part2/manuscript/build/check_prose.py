"""Prose checks for the manuscript source. Run: python check_prose.py ../part2_registered_tests.tex

Reports colons, semicolons and em-dashes outside commands that carry paths or
labels, control characters left by an eaten backslash, and the abstract's size.
"""
import re
import sys

BS = chr(92)
path = sys.argv[1]
src = open(path, encoding="utf-8").read()
body = src.split(BS + "begin{thebibliography}")[0].split(BS + "maketitle")[1]
strip = re.compile(r"\\(label|ref|cite|url|path|texttt|includegraphics|bibitem)(\[[^\]]*\])?\{[^}]*\}")
hits = 0
for i, line in enumerate(body.split("\n"), 1):
    if line.strip().startswith("%"):
        continue
    t = strip.sub("", line)
    t = re.sub(r"%.*", "", t)
    if re.search(r"[:;]|---", t):
        hits += 1
        print("PUNCT", i, t[:150])
print("colon/semicolon/em-dash lines:", hits)

raw = open(path, "rb").read().split(b"\n")
bad = [i for i, l in enumerate(raw, 1)
       if any(c in (l[:-1] if l.endswith(b"\r") else l) for c in b"\t\r\x0b\x0c\x07\x08")]
print("control-character lines:", bad)

m = re.search(r"begin\{abstract\}(.*?)\\end\{abstract\}", src, re.S)
a = m.group(1)
print("abstract words:", len(a.split()), "math marks:", a.count("$"))
