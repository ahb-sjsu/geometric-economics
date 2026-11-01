"""List every unescaped `$` immediately followed by a digit (or sign+digit) in
chapters/*.md and classify it as currency (needs `\\$`) or as the opening of a
genuine inline-math span. Run with --apply to escape the currency ones.

Heuristic: the span from the `$` to the next unescaped `$` on the same line is
"math" if it contains a TeX control sequence, `^`, `_`, or `\\` and no run of
two or more ordinary words separated by spaces; otherwise (or if there is no
closing `$`) it is currency.
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
FILES = sorted((ROOT / "chapters").glob("*.md")) + sorted((ROOT / "appendices").glob("*.md"))
PROSE = re.compile(r"[A-Za-z]{2,}\s+[a-z]{2,}\s+[a-z]{2,}")   # three prose words


def classify(span):
    if span is None:
        return "currency"
    if PROSE.search(span):
        return "currency"
    if re.search(r"\\|\^|_|[{}]", span):
        return "math"
    # pure arithmetic expression ending right at the closing $ (e.g. $9(9+1)/2 = 45$, $-3,420$)
    if re.fullmatch(r"[-+]?[0-9][0-9.,()+\-*/=<> ]*[0-9)]", span):
        return "math"
    # number then comparator then a variable (e.g. $1 < m < N$)
    if re.match(r"[-+]?[0-9.,]+\s*[<>=]\s*[A-Za-z]", span):
        return "math"
    # no space before the closing $ and no word of three or more letters (e.g. $1/(1 + kt)$)
    if re.search(r"[0-9A-Za-z)}]$", span) and not re.search(r"[A-Za-z]{3,}", span):
        return "math"
    return "currency"


def process(text, apply):
    out_lines = []
    report = []
    for ln, line in enumerate(text.split("\n"), 1):
        if line.startswith("```"):
            pass
        i = 0
        new = []
        in_math = False
        while i < len(line):
            c = line[i]
            if c == "\\" and i + 1 < len(line):
                new.append(line[i:i + 2]); i += 2; continue
            if c == "$":
                if in_math:
                    in_math = False; new.append(c); i += 1; continue
                m = re.match(r"\$([-+]?[0-9])", line[i:])
                if m:
                    # find next unescaped $
                    j = i + 1
                    close = None
                    while j < len(line):
                        if line[j] == "\\":
                            j += 2; continue
                        if line[j] == "$":
                            close = j; break
                        j += 1
                    span = line[i + 1:close] if close is not None else None
                    kind = classify(span)
                    report.append((ln, kind, line[max(0, i - 30):i + 45].replace("\n", " ")))
                    if kind == "currency":
                        new.append("\\$" if apply else "$"); i += 1; continue
                    in_math = True; new.append(c); i += 1; continue
                in_math = True; new.append(c); i += 1; continue
            new.append(c); i += 1
        out_lines.append("".join(new))
    return "\n".join(out_lines), report


def main():
    apply = "--apply" in sys.argv
    total = {"currency": 0, "math": 0}
    for f in FILES:
        text = f.read_text(encoding="utf-8")
        new, report = process(text, apply)
        for ln, kind, ctx in report:
            total[kind] += 1
            print(f"{f.name}:{ln}: [{kind}] {ctx}")
        if apply and new != text:
            f.write_text(new, encoding="utf-8", newline="\n")
    print(total)


if __name__ == "__main__":
    main()
