"""Figures for Chapters 1 to 16 of Geometric Economics.

Each figure is drawn from a formula, a definition or numbers printed in its chapter. The
volume is a posited framework (see the README): no economics instrument has passed the
series' admission filter. Where a chapter prints worked-example or hypothetical values the
caption says so, numbers the chapter reports from outside sources are given as the chapter's,
and schematics are labelled schematics. The earlier hand-drawn files figures/fig_NN_1_*.svg
are left untouched; these functions redraw the ideas from the chapter text.
"""

import math

from figkit import BORDER, BOX, CRITICAL, GRID, INK, INK2, INK3, SERIES, SURFACE, Axes, Canvas, legend, reg

DIMS = ["Consequences", "Rights", "Fairness", "Autonomy", "Trust", "Social impact", "Identity", "Legitimacy",
        "Epistemic"]
POSITED = "The values are the worked example's own, posited for illustration, not measurements."


# ------------------------------------------------------------------ helpers
def _poly(c, pts, col, width=2, dash=None, opacity=1.0, fill="none", fill_opacity=0.0):
    d = " ".join(f"{x:.2f},{y:.2f}" for x, y in pts)
    da = f' stroke-dasharray="{dash}"' if dash else ""
    c.add(f'<polyline points="{d}" fill="{fill}" fill-opacity="{fill_opacity}" stroke="{col}" stroke-width="{width}" '
          f'stroke-opacity="{opacity}" stroke-linejoin="round" stroke-linecap="round"{da}/>')


def _rect(c, x, y, w, h, fill, opacity=1.0, rx=0, stroke=None, sw=1):
    st = f' stroke="{stroke}" stroke-width="{sw}"' if stroke else ""
    c.add(f'<rect x="{x:.2f}" y="{y:.2f}" width="{max(w, 0.5):.2f}" height="{max(h, 0.5):.2f}" rx="{rx}" '
          f'fill="{fill}" fill-opacity="{opacity}"{st}/>')


def _circle(c, x, y, r, fill, opacity=1.0, stroke=None, width=1.5):
    st = f' stroke="{stroke}" stroke-width="{width}"' if stroke else ""
    c.add(f'<circle cx="{x:.2f}" cy="{y:.2f}" r="{r:.2f}" fill="{fill}" fill-opacity="{opacity}"{st}/>')


def _vbar(c, x, y0, w, dy, fill):
    """Signed vertical bar from the baseline y0; dy > 0 goes up."""
    if dy >= 0:
        _rect(c, x, y0 - dy, w, dy, fill, 1.0, 2)
    else:
        _rect(c, x, y0, w, -dy, fill, 1.0, 2)


def _hbar(c, x0, y, h, dx, fill):
    """Signed horizontal bar from the baseline x0; dx > 0 goes right."""
    if dx >= 0:
        _rect(c, x0, y, dx, h, fill, 1.0, 2)
    else:
        _rect(c, x0 + dx, y, -dx, h, fill, 1.0, 2)


def _note(c, s, h=400):
    c.text(16, h - 10, s, 10.5, "start", INK3, italic=True)


def _signed(v):
    return ("+" if v > 0 else "−" if v < 0 else "") + f"{abs(v):g}"


# ------------------------------------------------------------------ chapter 1
def fig_1_1():
    p = reg("chapters/ch01_the_scalar_economy.md", "1.1",
            "A schematic of the contraction that the chapter's Technical Appendix writes as GDP = sum over agents i and "
            "goods j of T(1, i, j). The economic tensor has one row of entries for each of the nine dimensions. GDP "
            "adds up the row for the monetary dimension and nothing else, so the other eight rows, and the way the "
            "rows interact, do not enter the number.",
            "### Failure 2: Utility Maximization")
    c = Canvas(720, 400, "GDP keeps one row of the economic tensor and discards eight")
    gx, gy, cw, rh, ncol = 190, 70, 22, 29, 12
    c.text(gx + ncol * cw / 2, gy - 10, "agent and good pairs (i, j)", 11, "middle", INK2)
    for k in range(9):
        y = gy + k * rh
        c.text(gx - 12, y + 18, f"d{k + 1}  {DIMS[k]}", 11.5, "end", INK if k == 0 else INK2)
        for j in range(ncol):
            if k == 0:
                _rect(c, gx + j * cw, y + 3, cw - 3, rh - 7, SERIES[0], 1.0, 3)
            else:
                _rect(c, gx + j * cw, y + 3, cw - 3, rh - 7, BOX, 1.0, 3, BORDER)
    x1 = gx + ncol * cw
    c.arrow(x1 + 6, gy + rh / 2, x1 + 46, gy + rh / 2, INK2, 1.5)
    c.box(x1 + 54, gy - 4, 200, 38, "GDP = Σ over i, j of T(1, i, j)", "the k = 1 row, summed")
    # bracket for the discarded rows
    bx = x1 + 12
    ytop, ybot = gy + rh + 4, gy + 9 * rh - 4
    _poly(c, [(bx, ytop), (bx + 10, ytop), (bx + 10, ybot), (bx, ybot)], INK3, 1.5)
    ym = (ytop + ybot) / 2
    c.text(bx + 24, ym - 20, "k = 2, …, 9", 12.5, "start", INK, "600")
    c.text(bx + 24, ym, "not in the sum: the contraction", 11, "start", INK2)
    c.text(bx + 24, ym + 16, "discards these components and", 11, "start", INK2)
    c.text(bx + 24, ym + 32, "how the dimensions interact", 11, "start", INK2)
    legend(c, gx, 352, [("entries GDP adds up", SERIES[0]), ("entries GDP does not see", BOX)])
    _note(c, "schematic of the contraction formula; the cells stand for tensor components, not data")
    c.save(p)


# ------------------------------------------------------------------ chapter 2
def fig_2_1():
    rows = [
        ("Classical rational choice", [(1944, "von Neumann, Morgenstern")], "the study of d1"),
        ("Game theory", [(1950, "Nash")], "interaction on the scalar projection"),
        ("Social choice", [(1951, "Arrow"), (1999, "Sen")], "dimensional collapse and its consequences"),
        ("Bounded rationality", [(1955, "Simon")], "heuristic-guided search"),
        ("Experimental economics", [(1962, "Smith")], "laboratory measurement of manifold structure"),
        ("Information economics", [(1970, "Akerlof")], "the study of d9 miscalibration"),
        ("Prospect theory", [(1979, "Kahneman, Tversky")], "metric asymmetry, curvature, gauge violations"),
        ("Commons governance", [(1990, "Ostrom")], "boundary-penalty maintenance"),
        ("Moral foundations theory", [(2012, "Haidt")], "catalogue of the heuristic function's content"),
    ]
    p = reg("chapters/ch02_historical_precursors.md", "2.1",
            "The nine schools of Sections 2.1 to 2.9, each placed at the year of the work the chapter cites for it, "
            "with the part of the geometric framework that Section 2.10 assigns to it. This is a schematic of the "
            "chapter's reading of the literature, not a result: the right-hand column is the book's interpretation "
            "of each school.",
            "## Technical Appendix")
    c = Canvas(720, 430, "Nine schools, and the piece of the geometry each is read as")
    x0, x1, y0, rh = 200, 420, 84, 34
    X = lambda yr: x0 + (x1 - x0) * (yr - 1940) / 80.0  # noqa: E731
    for yr in (1940, 1960, 1980, 2000, 2020):
        c.line(X(yr), y0 - 8, X(yr), y0 + rh * len(rows), GRID, 1)
        c.text(X(yr), y0 - 14, str(yr), 10.5, "middle", INK2)
    c.text(18, y0 - 14, "School", 11, "start", INK3, italic=True)
    c.text(446, y0 - 14, "Read in Section 2.10 as", 11, "start", INK3, italic=True)
    for i, (name, marks, reading) in enumerate(rows):
        y = y0 + rh * i + rh / 2
        c.line(18, y + rh / 2, 702, y + rh / 2, GRID, 1)
        c.text(18, y + 4, name, 11.5, "start", INK)
        if len(marks) == 2:
            c.line(X(marks[0][0]), y, X(marks[1][0]), y, INK3, 1.5)
        for yr, who in marks:
            c.dot(X(yr), y, SERIES[i % 8], 4.5, title=f"{who} ({yr})")
        yr, who = marks[0]
        if len(marks) == 1:
            if yr < 1975:
                c.text(X(yr) + 10, y + 4, f"{who} {yr}", 10, "start", INK2)
            else:
                c.text(X(yr) - 10, y + 4, f"{who} {yr}", 10, "end", INK2)
        else:
            c.text((X(marks[0][0]) + X(marks[1][0])) / 2, y - 6, "Arrow 1951, Sen 1999", 10, "middle", INK2)
        c.text(446, y + 4, reading, 11, "start", INK2)
    _note(c, "schematic of the chapter's reading; years are those of the works the chapter cites", 430)
    c.save(p)


# ------------------------------------------------------------------ chapter 3
def fig_3_1():
    rows = [
        ("Consequences", "monetary cost, material outcome", ""),
        ("Rights / Entitlements", "property rights, contracts", "Can I be punished for this?"),
        ("Fairness", "distributional and procedural justice", ""),
        ("Autonomy", "freedom of choice, voluntariness", ""),
        ("Privacy / Trust", "information asymmetry, fiduciary duty", ""),
        ("Social impact", "externalities, reputation", "Will this damage my reputation?"),
        ("Virtue / Identity", "self-image, character consistency", ""),
        ("Legitimacy", "institutional trust, rule compliance", "Will the contract be enforced?"),
        ("Epistemic status", "information quality, ambiguity", "Do I have enough information?"),
    ]
    p = reg("chapters/ch03_decision_manifold.md", "3.1",
            "The nine dimensions of Definition 1. The first is the only one visible to Homo economicus. Remark 1 "
            "argues that four of the others, marked here with the question the chapter attaches to each, are "
            "information a purely selfish agent must also process. This is a schematic of the definition, not data.",
            "### The Transferable/Evaluative Distinction")
    c = Canvas(720, 440, "Nine dimensions: Homo economicus sees one, any egoist needs five")
    y0, rh = 64, 37
    c.text(64, y0 - 8, "Dimension", 11, "start", INK3, italic=True)
    c.text(236, y0 - 8, "What it records (Definition 1)", 11, "start", INK3, italic=True)
    c.text(478, y0 - 8, "A selfish agent still asks (Remark 1)", 11, "start", INK3, italic=True)
    for k, (name, what, q) in enumerate(rows):
        y = y0 + k * rh
        col = SERIES[0] if k == 0 else (SERIES[1] if q else BOX)
        _rect(c, 18, y + 4, 36, rh - 9, col, 1.0, 5, BORDER if col == BOX else None)
        c.text(36, y + rh / 2 + 4, f"d{k + 1}", 12, "middle", SURFACE if col != BOX else INK, "600")
        c.text(64, y + rh / 2 + 4, name, 12, "start", INK, "600")
        c.text(236, y + rh / 2 + 4, what, 11, "start", INK2)
        if k == 0:
            c.text(478, y + rh / 2 + 4, "the only dimension Homo economicus sees", 11, "start", INK)
        elif q:
            c.text(478, y + rh / 2 + 4, q, 11, "start", INK)
        c.line(18, y + rh, 702, y + rh, GRID, 1)
    legend(c, 18, 414, [("visible to Homo economicus", SERIES[0]), ("needed even by a selfish agent", SERIES[1]),
                        ("the other four", BOX)])
    c.save(p)


def fig_3_2():
    v = {
        "v1: accept 7,000 a month": [+0.3, -0.5, -0.4, -0.6, -0.2, -0.3, +0.2, -0.5],
        "v2: negotiate 6,000, five-year term": [+0.7, +0.1, -0.1, +0.2, +0.1, +0.2, +0.3, +0.4],
        "v3: close the shop": [-0.8, -0.3, -0.7, -0.4, -0.9, -0.8, 0.0, +0.3],
    }
    assert 12 * 2000 == 24000 and 12 * 1000 == 12000       # the d1 entries of the two priced options
    p = reg("chapters/ch03_decision_manifold.md", "3.2",
            "The three lease options of Section 3.8 as the chapter writes them: the change in each of the dimensions "
            "d2 to d9 relative to the current lease, on the chapter's own scale. The monetary change d1 is given "
            "under each name in dollars over twelve months. Accepting the increase and closing the shop are negative "
            "on most dimensions, and the negotiated lease is positive on seven of the eight. " + POSITED,
            "### Computing Edge Weights")
    c = Canvas(720, 420, "Three lease options: the non-monetary changes each one carries")
    ax = Axes(c, 60, 92, 640, 240, (0, 8), (-1, 1), (), [-1, -0.5, 0, 0.5, 1], "", "")
    c.text(18, 212, "change relative to current lease", 11, "middle", INK2, rotate=-90)
    slot = ax.w / 8
    bw = 16
    base = ax.Y(0)
    c.line(ax.x0, base, ax.x0 + ax.w, base, INK3, 1)
    for k in range(8):
        cx = ax.x0 + slot * (k + 0.5)
        for j, vals in enumerate(v.values()):
            x = cx - (3 * bw + 4) / 2 + j * (bw + 2)
            val = vals[k]
            if val == 0:
                c.line(x, base, x + bw, base, SERIES[j], 3)
            else:
                _vbar(c, x, base, bw, base - ax.Y(val), SERIES[j])
        c.text(cx, ax.y0 + ax.h + 18, f"d{k + 2}", 11.5, "middle", INK)
        c.text(cx, ax.y0 + ax.h + 33, DIMS[k + 1], 10, "middle", INK2)
    d1 = ["d1 = −24,000", "d1 = −12,000", "d1 = +savings (no figure given)"]
    xs = [60, 262, 520]
    for j, name in enumerate(v):
        c.add(f'<rect x="{xs[j]}" y="45" width="12" height="12" rx="3" fill="{SERIES[j]}"/>')
        c.text(xs[j] + 18, 55, name, 11.5, "start", INK)
        c.text(xs[j] + 18, 71, d1[j], 10.5, "start", INK2)
    _note(c, "values printed in Section 3.8; a worked example, not measured data", 420)
    c.save(p)


# ------------------------------------------------------------------ chapter 4
def fig_4_1():
    gain = [0, +0.2, +0.1, +0.1, +0.1, +0.1, 0, 0]
    loss = [-0.3, -0.6, -0.5, -0.7, -0.4, -0.5, +0.1, -0.6]
    assert abs(sum(g * g for g in gain) - 0.08) < 1e-12     # "add approximately 8%" in the worked example
    assert 12 * 2000 == 24000
    p = reg("chapters/ch04_economic_metric.md", "4.1",
            "The two paths of the worked example in Section 4.8. The rent falls or rises by the same 2,000 dollars a "
            "month, 24,000 a year, so the monetary change d1 has the same size on both paths. The bars show the "
            "changes the chapter assigns on the other eight dimensions: small for the gain, and larger on seven "
            "dimensions for the loss. This asymmetry is what the chapter's account of loss aversion rests on. "
            + POSITED,
            "### Computing Edge Weights")
    c = Canvas(720, 420, "The same 24,000 dollars: a loss moves more dimensions than a gain")
    ax = Axes(c, 190, 80, 420, 268, (-0.8, 0.4), (0, 8), [-0.8, -0.6, -0.4, -0.2, 0, 0.2, 0.4], [],
              "change on the dimension (the chapter's scale)", "")
    for t in (-0.8, -0.6, -0.4, -0.2, 0.2, 0.4):
        c.line(ax.X(t), ax.y0, ax.X(t), ax.y0 + ax.h, GRID, 1)
    x0 = ax.X(0)
    c.line(x0, ax.y0, x0, ax.y0 + ax.h, INK3, 1)
    rh = ax.h / 8
    for k in range(8):
        y = ax.y0 + rh * k
        c.text(ax.x0 - 12, y + rh / 2 + 4, f"d{k + 2}  {DIMS[k + 1]}", 11.5, "end", INK2)
        g, l_ = gain[k], loss[k]
        if g:
            _hbar(c, x0, y + 5, 11, ax.X(g) - x0, SERIES[0])
        else:
            c.line(x0, y + 5, x0, y + 16, SERIES[0], 3)
        _hbar(c, x0, y + 18, 11, ax.X(l_) - x0, SERIES[1])
        c.text(ax.X(g) + 7 if g else x0 + 7, y + 14.5, _signed(g) if g else "0", 10, "start", INK)
        if l_ < 0:
            c.text(ax.X(l_) - 7, y + 27.5, _signed(l_), 10, "end", INK)
        else:
            c.text(ax.X(l_) + 7, y + 27.5, _signed(l_), 10, "start", INK)
    legend(c, 190, 48, [("gain path: rent falls to 3,000 a month (d1 = +24,000 a year)", SERIES[0])], 11)
    legend(c, 190, 66, [("loss path: rent rises to 7,000 a month (d1 = −24,000 a year)", SERIES[1])], 11)
    _note(c, "vectors printed in Section 4.8; a worked example, not measured data", 420)
    c.save(p)


# ------------------------------------------------------------------ chapter 5
def fig_5_1():
    base = 1400
    margin = {"B": base + 2580, "C": base + 600, "D": base + 4200}
    assert margin == {"B": 3980, "C": 2000, "D": 5600}      # the margins the chapter prints
    names = {"A": "A  absorb the cost", "B": "B  pass it all on (5.50 a cup)",
             "C": "C  5.00 a cup and negotiate", "D": "D  switch to a cheaper supplier"}
    left = ["D", "B", "C", "A"]                             # Step 4: d1-only ranking D > B > C > A
    right = ["C", "B", "A", "D"]                            # Step 4: full-manifold ranking C > B > A > D
    assert sorted(margin, key=margin.get, reverse=True) == left[:3]
    col = {k: SERIES[i] for i, k in enumerate("ABCD")}
    lsub = {"D": "margin 5,600 a month", "B": "margin 3,980 a month", "C": "margin 2,000 a month",
            "A": "margin turns negative"}
    rsub = {"C": "no boundary crossed", "B": "fairness boundary crossed", "A": "business closes, community hub lost",
            "D": "trust boundary: h is infinite"}
    p = reg("chapters/ch05_price_as_heuristic.md", "5.1",
            "Maria's four pricing paths from the worked example, ranked twice as Step 4 ranks them: on the left by "
            "the monetary dimension alone, on the right by f = g + h on the full manifold. Margins are the chapter's, "
            "in dollars a month. The path that is best on money, switching supplier, is last on the full manifold "
            "because the chapter assigns it an infinite trust penalty, and the path chosen is third on money. "
            + POSITED,
            "## Heuristic Fields Over the Decision Complex")
    c = Canvas(720, 400, "Maria's pricing paths: the ranking on money and on the full manifold")
    xl, xr, y0, rh = 262, 458, 110, 62
    c.text(xl, 66, "Ranked on d1 alone", 12.5, "end", INK, "600")
    c.text(xl, 82, "(what the scalar economist sees)", 10.5, "end", INK2)
    c.text(xr, 66, "Ranked on the full manifold", 12.5, "start", INK, "600")
    c.text(xr, 82, "(f = g + h, Step 3)", 10.5, "start", INK2)
    for r in range(4):
        y = y0 + r * rh
        c.text(30, y + 4, ["1st", "2nd", "3rd", "4th"][r], 11, "start", INK3)
        c.text(700, y + 4, ["1st", "2nd", "3rd", "4th"][r], 11, "end", INK3)
    for k in "ABCD":
        yl, yr = y0 + left.index(k) * rh, y0 + right.index(k) * rh
        c.line(xl + 14, yl, xr - 14, yr, col[k], 2.5)
        c.dot(xl + 14, yl, col[k], 5)
        c.dot(xr - 14, yr, col[k], 5)
        c.text(xl, yl - 2, names[k], 11.5, "end", INK)
        c.text(xl, yl + 13, lsub[k], 10.5, "end", INK2)
        c.text(xr, yr - 2, names[k], 11.5, "start", INK)
        c.text(xr, yr + 13, rsub[k], 10.5, "start", INK2)
    _note(c, "worked example of Chapter 5; rankings as stated in Step 4")
    c.save(p)


# ------------------------------------------------------------------ chapter 6
def fig_6_1():
    def phi(x, y):
        return x + 0.15 * math.sin(2 * math.pi * y)

    ya, yb, lev = 0.2, 0.8, 0.5
    a = (lev - 0.15 * math.sin(2 * math.pi * ya), ya)
    b = (lev - 0.15 * math.sin(2 * math.pi * yb), yb)
    assert abs(phi(*a) - phi(*b)) < 1e-12 and a != b       # two different states, one scalar value
    p = reg("chapters/ch06_economic_tensors.md", "6.1",
            "Part 1 of Theorem 14 in a picture with two dimensions instead of nine. The curves are level sets of one "
            "illustrative continuous function, phi(a1, a2) = a1 + 0.15 sin(2 pi a2): every state on a curve gets the "
            "same number. The states a and a' differ on the second dimension and both map to 0.5, so the number "
            "cannot tell them apart and no rule can recover the state from it. In nine dimensions the chapter's "
            "level sets have dimension at least 8.",
            "### What the Theorem Says")
    c = Canvas(720, 400, "A scalar sends whole level sets of states to one number")
    ax = Axes(c, 70, 56, 330, 280, (0, 1), (0, 1), [0, 0.25, 0.5, 0.75, 1], [0, 0.25, 0.5, 0.75, 1],
              "a1 (the monetary dimension)", "a2 (another dimension)")
    for lv in (0.1, 0.3, 0.5, 0.7, 0.9):
        pts = []
        for i in range(101):
            y = i / 100
            x = lv - 0.15 * math.sin(2 * math.pi * y)
            if 0 <= x <= 1:
                pts.append((ax.X(x), ax.Y(y)))
        if lv == lev:
            _poly(c, pts, SERIES[0], 2.5)
        else:
            _poly(c, pts, INK3, 1.2, opacity=0.7)
    # the scalar line
    lx, ly0, ly1 = 560, 76, 316
    c.line(lx, ly0, lx, ly1, INK2, 1.5)
    Yl = lambda v: ly1 - (ly1 - ly0) * v  # noqa: E731
    for v in (0, 0.25, 0.5, 0.75, 1):
        c.line(lx - 4, Yl(v), lx + 4, Yl(v), INK2, 1.5)
        c.text(lx + 12, Yl(v) + 4, f"{v:g}", 11, "start", INK2)
    c.text(lx, ly0 - 12, "the scalar phi", 11.5, "middle", INK)
    for pt, lab, dy in ((a, "a", 18), (b, "a'", -8)):
        px, py = ax.X(pt[0]), ax.Y(pt[1])
        c.line(px, py, lx - 8, Yl(lev), SERIES[1], 1.5, dash="5 4")
        c.dot(px, py, SERIES[1], 5, title=f"{lab} = ({pt[0]:.3f}, {pt[1]:.1f}), phi = 0.5")
        c.text(px - 12, py + dy, lab, 13, "end", INK, "600", italic=True)
    c.dot(lx, Yl(lev), SERIES[1], 5.5)
    c.text(lx + 40, Yl(lev) + 4, "= phi(a) = phi(a')", 11, "start", INK)
    c.line(436, 352, 460, 352, SERIES[0], 2.5)
    c.text(468, 356, "level set phi = 0.5", 11, "start", INK2)
    c.line(590, 352, 614, 352, INK3, 1.2)
    c.text(622, 356, "other levels", 11, "start", INK2)
    _note(c, "illustrative function in two dimensions; the theorem is for any continuous map from nine dimensions to one")
    c.save(p)


def fig_6_2():
    B = [0.7, 0.8, 0.6, 0.9, 0.85, 0.9, 0.7, 0.4]          # B2 ... B9 of the running example
    gut = {3, 5, 6, 7}                                     # components the chapter says the buyer destroys
    p = reg("chapters/ch06_economic_tensors.md", "6.2",
            "The tensor valuation of Maria's coffee shop from the chapter's running example. The appraiser reports "
            "one component, B1 = 200,000 dollars. The bars are the other eight components on the chapter's scale "
            "from 0 to 1. The four in the second colour are the ones the chapter says a buyer could destroy while "
            "B1 stays the same or rises, a change the scalar valuation would not show. " + POSITED,
            "## Worked Example: Maria's Valuation Under Different Projections")
    c = Canvas(720, 420, "One number is reported; eight components of the valuation are not")
    c.box(18, 46, 200, 42, "B1 = 200,000 dollars", "DCF valuation: the reported scalar", BOX, SERIES[0])
    ax = Axes(c, 190, 112, 420, 248, (0, 1), (0, 8), [0, 0.2, 0.4, 0.6, 0.8, 1.0], [],
              "component value (the chapter's scale, 0 to 1)", "")
    for t in (0.2, 0.4, 0.6, 0.8, 1.0):
        c.line(ax.X(t), ax.y0, ax.X(t), ax.y0 + ax.h, GRID, 1)
    rh = ax.h / 8
    for k in range(8):
        y = ax.y0 + rh * k
        col = SERIES[1] if (k + 2) in gut else SERIES[0]
        c.text(ax.x0 - 12, y + rh / 2 + 4, f"B{k + 2}  {DIMS[k + 1]}", 11.5, "end", INK2)
        c.hrect(ax.x0, y + 7, ax.X(B[k]) - ax.x0, rh - 14, col, title=f"B{k + 2} = {B[k]}")
        c.text(ax.X(B[k]) + 8, y + rh / 2 + 4, f"{B[k]:g}", 10.5, "start", INK)
    legend(c, 250, 72, [("not reported", SERIES[0]), ("not reported, and lost if the buyer guts the business",
                                                      SERIES[1])], 11)
    _note(c, "running example of Chapter 6; assessed values, not measurements", 420)
    c.save(p)


# ------------------------------------------------------------------ chapter 7
def fig_7_1():
    L = ["5K, no change", "6K", "6K + 5-year guarantee", "7K", "7K + buyout offer"]
    M = ["Accept any", "Accept ≤ 6K", "Accept ≤ 6K", "Reject all", "Negotiate +"]
    M2 = ["offer", "only", "with guarantee", "increases", "campaign"]
    lbr = {0: 2, 1: 1, 2: 2, 3: 0, 4: 2}                   # Step 1: landlord's best response to each column
    mbr = {2: 2, 3: 4, 4: 4}                               # Step 2: rows where the chapter names Maria's strategy
    fixed = [(r, col) for col, r in lbr.items() if mbr.get(r) == col]
    assert fixed == [(2, 2)]                               # Step 3: 6K + guarantee, accept with guarantee
    p = reg("chapters/ch07_bond_geodesic_equilibrium.md", "7.1",
            "The best responses that the worked example lists for the lease negotiation. A filled circle marks the "
            "landlord's best response to each of Maria's strategies (Step 1), and a ring marks Maria's best response "
            "to each rent offer where the chapter names one (Step 2). For the offers of 5K and 6K the chapter says "
            "only that Maria accepts. Both marks fall in one cell, 6K with a five-year guarantee and acceptance with "
            "guarantee, which the chapter takes as the Bond geodesic equilibrium. " + POSITED,
            "### Checking the contraction condition")
    c = Canvas(720, 420, "Lease negotiation: where the two best responses coincide")
    gx, gy, cw, rh = 188, 116, 92, 48
    c.text(gx + 2.5 * cw, 58, "Maria's strategy", 12, "middle", INK, "600")
    c.text(18, gy - 12, "Landlord's offer", 12, "start", INK, "600")
    for j in range(5):
        c.text(gx + (j + 0.5) * cw, 82, M[j], 10.5, "middle", INK2)
        c.text(gx + (j + 0.5) * cw, 96, M2[j], 10.5, "middle", INK2)
    for i in range(5):
        y = gy + i * rh
        c.text(gx - 12, y + rh / 2 + 4, L[i], 11, "end", INK2)
        for j in range(5):
            x = gx + j * cw
            hit = (i, j) in fixed
            _rect(c, x + 2, y + 2, cw - 4, rh - 4, BOX, 1.0, 5, CRITICAL if hit else BORDER, 2 if hit else 1)
            if lbr[j] == i:
                _circle(c, x + cw / 2 - (11 if hit else 0), y + rh / 2, 7, SERIES[0])
            if mbr.get(i) == j:
                _circle(c, x + cw / 2 + (11 if hit else 0), y + rh / 2, 7, SURFACE, 0.0, SERIES[1], 3)
        if i not in mbr:
            c.text(gx + 5 * cw + 8, y + rh / 2 + 4, "Maria accepts", 10, "start", INK3, italic=True)
    c.text(gx + 2.5 * cw, gy + 3 * rh - 5, "equilibrium", 9.5, "middle", INK)
    _circle(c, 196, 384, 6, SERIES[0])
    c.text(208, 388, "landlord's best response to the column", 11, "start", INK2)
    _circle(c, 452, 384, 6, SURFACE, 0.0, SERIES[1], 3)
    c.text(464, 388, "Maria's best response to the row", 11, "start", INK2)
    _note(c, "best responses as listed in Steps 1 to 3 of the worked example", 420)
    c.save(p)


# ------------------------------------------------------------------ chapter 8
def fig_8_1():
    rows = [("48,000 a year", "baseline", 6.2), ("4,000 a month", "unit scaling", 5.8),
            ("23.08 an hour", "unit scaling", 5.1), ("49,440 a year after", "3% inflation", 7.1)]
    se = 0.3
    assert abs(48000 / 12 - 4000) < 1e-9 and round(48000 / 2080, 2) == 23.08 and round(48000 * 1.03) == 49440
    V = [round(r[2] - rows[0][2], 1) for r in rows[1:]]
    assert V == [-0.4, -1.1, 0.9]
    norm = math.sqrt(sum(x * x for x in V))
    assert round(norm, 2) == 1.48
    p = reg("chapters/ch08_gauge_invariance.md", "8.1",
            "The worked example of Section 8.7: one real salary described four ways, with the mean attractiveness "
            "rating on a scale of 1 to 10 that the chapter supplies for each description, plus or minus one standard "
            "error. The chapter states that these ratings are hypothetical. The differences from the baseline are "
            "the components of the gauge violation tensor, −0.4, −1.1 and +0.9, with Frobenius norm 1.48; a "
            "description-invariant evaluation would put all four points on the dashed line.",
            "## 8.8 The Geometry of Gauge Correction")
    c = Canvas(720, 400, "One salary, four descriptions: the hypothetical ratings differ")
    ax = Axes(c, 70, 56, 600, 250, (0, 4), (4, 8), (), [4, 5, 6, 7, 8], "", "mean attractiveness (scale 1 to 10)")
    yb = ax.Y(rows[0][2])
    c.line(ax.x0, yb, ax.x0 + ax.w, yb, INK3, 1.5, dash="4 4")
    c.text(ax.x0 + ax.w, yb - 6, "baseline 6.2: no gauge violation", 10.5, "end", INK2, italic=True)
    for i, (a, b, m) in enumerate(rows):
        x = ax.x0 + ax.w * (i + 0.5) / 4
        col = SERIES[0] if i == 0 else SERIES[1]
        c.line(x, ax.Y(m - se), x, ax.Y(m + se), col, 2)
        for e in (m - se, m + se):
            c.line(x - 6, ax.Y(e), x + 6, ax.Y(e), col, 2)
        c.dot(x, ax.Y(m), col, 5.5, title=f"{a} {b}: {m} ± {se}")
        c.text(x + 14, ax.Y(m) + (-8 if i == 0 else 4), f"{m:g}", 11.5, "start", INK, "600")
        if i:
            c.text(x + 14, ax.Y(m) + 19, f"V = {_signed(V[i - 1])}", 10.5, "start", INK2)
        c.text(x, ax.y0 + ax.h + 18, a, 11, "middle", INK)
        c.text(x, ax.y0 + ax.h + 33, b, 10.5, "middle", INK2)
    c.text(ax.x0 + ax.w / 2, 362, f"Frobenius norm of V = √(0.4² + 1.1² + 0.9²) ≈ {norm:.2f}", 11.5, "middle", INK)
    _note(c, "hypothetical results, as the chapter states; whiskers are ± 1 standard error (0.3)")
    c.save(p)


# ------------------------------------------------------------------ chapter 9
def fig_9_1():
    rows = [("d5 Trust", 0.3, 0.4, 0.7), ("d6 Community", 0.2, 0.3, 0.5), ("d7 Identity", 0.4, 0.5, 0.9),
            ("d9 Epistemic", 0.2, 0.1, 0.3)]
    for _, m, e, s in rows:
        assert abs(m + e - s) < 1e-9
    total = sum(r[3] for r in rows)
    assert abs(total - 2.4) < 1e-9 and 80 * 25 == 2000
    p = reg("chapters/ch09_conservation_laws.md", "9.1",
            "The worked example of Maria's order from Elena, 80 pounds at 25 dollars a pound. On the left the money: "
            "Maria pays 2,000 dollars and Elena receives 2,000, and the two changes sum to zero. On the right the "
            "four evaluative dimensions the example lists: both parties gain on each, and the gains sum to 2.4 units "
            "on the chapter's scale. " + POSITED,
            "### What Conservation Reveals About This Transaction")
    c = Canvas(720, 400, "The money sums to zero; the evaluative changes do not")
    # left panel: d1
    ax1 = Axes(c, 78, 86, 150, 230, (0, 2), (-2500, 2500), (), [], "", "")
    for t in (-2000, -1000, 0, 1000, 2000):
        c.line(ax1.x0, ax1.Y(t), ax1.x0 + ax1.w, ax1.Y(t), GRID, 1)
        c.text(ax1.x0 - 8, ax1.Y(t) + 4, f"{t:,}".replace("-", "−"), 11, "end", INK2)
    b1 = ax1.Y(0)
    c.line(ax1.x0, b1, ax1.x0 + ax1.w, b1, INK3, 1)
    for i, (nm, val) in enumerate((("Maria", -2000), ("Elena", 2000))):
        x = ax1.x0 + 75 * (i + 0.5) - 11
        _vbar(c, x, b1, 22, b1 - ax1.Y(val), SERIES[i])
        c.text(x + 11, ax1.Y(val) + (16 if val < 0 else -7), _signed(val).replace("2000", "2,000"), 11, "middle", INK)
    c.text(ax1.x0 + ax1.w / 2, 66, "d1 Money (dollars)", 12, "middle", INK, "600")
    c.text(ax1.x0 + ax1.w / 2, 362, "sum = 0", 12, "middle", INK, "600")
    # right panel: evaluative, stacked
    ax2 = Axes(c, 320, 86, 370, 230, (0, 4), (0, 1), (), [0, 0.2, 0.4, 0.6, 0.8, 1.0], "", "")
    for i, (nm, m, e, s) in enumerate(rows):
        x = ax2.x0 + ax2.w * (i + 0.5) / 4 - 12
        y1, y2 = ax2.Y(m), ax2.Y(m + e)
        _rect(c, x, y1, 24, ax2.Y(0) - y1, SERIES[0])
        c.rect(x, y2, 24, y1 - y2 - 2, SERIES[1], title=f"{nm}, Elena +{e}")
        c.text(x + 34, (ax2.Y(0) + y1) / 2 + 4, f"+{m:g}", 10.5, "start", INK2)
        c.text(x + 34, (y1 + y2) / 2 + 3, f"+{e:g}", 10.5, "start", INK2)
        c.text(x + 12, y2 - 8, f"sum +{s:g}", 11, "middle", INK, "600")
        c.text(x + 12, ax2.y0 + ax2.h + 18, nm, 11, "middle", INK2)
    c.text(ax2.x0 + ax2.w / 2, 66, "Evaluative dimensions (the chapter's units)", 12, "middle", INK, "600")
    c.text(ax2.x0 + ax2.w / 2, 362, f"sum over the four = +{total:.1f}", 12, "middle", INK, "600")
    legend(c, 300, 46, [("Maria (buyer)", SERIES[0]), ("Elena (seller)", SERIES[1])])
    _note(c, "worked example of Chapter 9; values assigned by the chapter, not measured")
    c.save(p)


# ------------------------------------------------------------------ chapter 10
def fig_10_1():
    boxes = [
        ("Heuristic corruption", "the gradient of h points away from the geodesic",
         "externalities, information asymmetry", "2008: securities priced by models that ignored tail risk"),
        ("Objective hijacking", "the search optimizes the wrong objective",
         "regulatory capture, short-termism", "2008: rating agencies dependent on issuers' fees"),
        ("Local minima", "the search is trapped in a suboptimal basin",
         "bubbles, poverty traps", "2008: the housing bubble, no one willing to exit first"),
        ("Gauge breaking", "the output depends on description, not content",
         "money illusion, framing effects", "2008: nominal house prices rose, real ones did not"),
    ]
    pos = [(18, 62), (372, 62), (372, 262), (18, 262)]      # clockwise: 1 top-left, 2 top-right, 3 bottom-right, 4
    bw, bh = 330, 112
    p = reg("chapters/ch10_market_failures.md", "10.1",
            "The four pathologies of Section 10.1 arranged in the cycle of Proposition 10.2, in which each one "
            "enables or deepens the next. Each box gives the general form, the economic instances from the "
            "chapter's table, and the step the chapter assigns to it in its account of the 2008 crisis. This is a "
            "schematic of the chapter's proposal; Section 16.4 lists the cascade as a prediction still to be tested.",
            "## Worked Example: Maria's Gentrifying Neighborhood")
    c = Canvas(720, 420, "Four pathologies of market search, and the cycle proposed among them")
    for i, ((name, form, econ, y08), (x, y)) in enumerate(zip(boxes, pos)):
        _rect(c, x, y, bw, bh, BOX, 1.0, 6, BORDER)
        c.add(f'<rect x="{x}" y="{y}" width="{bw}" height="4" rx="2" fill="{SERIES[i]}"/>')
        c.text(x + 14, y + 27, f"{i + 1}. {name}", 13.5, "start", INK, "600")
        c.text(x + 14, y + 48, form, 11, "start", INK2)
        c.text(x + 14, y + 66, econ, 11, "start", INK)
        c.line(x + 14, y + 78, x + bw - 14, y + 78, BORDER, 1)
        c.text(x + 14, y + 97, y08, 10.5, "start", INK2)
    c.arrow(350, 118, 370, 118, INK, 2)                    # 1 -> 2
    c.arrow(537, 176, 537, 258, INK, 2)                    # 2 -> 3
    c.arrow(370, 318, 350, 318, INK, 2)                    # 3 -> 4
    c.arrow(183, 260, 183, 178, INK, 2)                    # 4 -> 1
    c.text(360, 214, "each enables or deepens the next", 11.5, "middle", INK)
    c.text(360, 231, "(Proposition 10.2)", 10.5, "middle", INK2)
    _note(c, "schematic of the chapter's taxonomy and proposed cascade; not a measured result", 420)
    c.save(p)


# ------------------------------------------------------------------ chapter 11
def fig_11_1():
    rhos = [i / 200 for i in range(0, 200)]

    def det(r):
        return 1 - r * r

    def cost(r):
        # u = (1, -1)/sqrt(2); u^T Sigma^{-1} u for Sigma = [[1, r], [r, 1]]
        inv = [[1 / det(r), -r / det(r)], [-r / det(r), 1 / det(r)]]
        u = (1 / math.sqrt(2), -1 / math.sqrt(2))
        return sum(u[i] * inv[i][j] * u[j] for i in range(2) for j in range(2))

    for r in (0.0, 0.5, 0.9, 0.99):
        assert abs(cost(r) - 1 / (1 - r)) < 1e-9          # closed form of the quadratic form
    p = reg("chapters/ch11_financial_crises.md", "11.1",
            "The degeneracy of Definition 38 in the smallest case: two dimensions with unit variances and correlation "
            "rho, so that the covariance matrix is [[1, rho], [rho, 1]]. Left, its determinant, 1 − rho squared, "
            "falls to zero as the correlation goes to 1. Right, on a logarithmic scale, the cost that the metric "
            "g, the inverse of the covariance matrix, assigns to a unit displacement in the direction that moves "
            "the two dimensions oppositely: it equals 1/(1 − rho) and grows without bound. Computed from the "
            "chapter's formulas for an illustrative two-dimensional case.",
            "### Curvature Diverges")
    c = Canvas(720, 400, "As correlations approach 1 the covariance matrix degenerates")
    ax1 = Axes(c, 70, 70, 260, 250, (0, 1), (0, 1), [0, 0.25, 0.5, 0.75, 1], [0, 0.25, 0.5, 0.75, 1],
               "correlation rho", "det Σ")
    _poly(c, [(ax1.X(r), ax1.Y(det(r))) for r in rhos + [1.0]], SERIES[0], 2.5)
    c.text(ax1.x0 + 8, ax1.y0 - 10, "det Σ = 1 − rho²", 12, "start", INK, "600")
    c.text(ax1.X(0.62), ax1.Y(0.80), "→ 0: the inverse", 10.5, "start", INK2)
    c.text(ax1.X(0.62), ax1.Y(0.80) + 15, "ceases to exist", 10.5, "start", INK2)
    ax2 = Axes(c, 420, 70, 260, 250, (0, 1), (1, 1000), [0, 0.25, 0.5, 0.75, 1], [], "correlation rho", "", ylog=True)
    for v in (1, 10, 100, 1000):
        c.line(ax2.x0, ax2.Y(v), ax2.x0 + ax2.w, ax2.Y(v), GRID, 1)
        c.text(ax2.x0 - 8, ax2.Y(v) + 4, f"{v:,}", 11, "end", INK2)
    pts = [(ax2.X(r), ax2.Y(cost(r))) for r in [i / 1000 for i in range(0, 1000)] if cost(r) <= 1000]
    _poly(c, pts, SERIES[1], 2.5)
    c.text(ax2.x0 + 8, ax2.y0 - 10, "cost of a unit move, u = (1, −1)/√2", 12, "start", INK, "600")
    c.text(ax2.x0 - 46, ax2.y0 + ax2.h / 2, "uᵀ Σ⁻¹ u", 11.5, "middle", INK2, rotate=-90)
    for r in (0.9, 0.99):
        c.dot(ax2.X(r), ax2.Y(cost(r)), SERIES[1], 4.5, title=f"rho = {r}: cost {cost(r):.0f}")
        c.text(ax2.X(r) - 10, ax2.Y(cost(r)) - 6, f"rho = {r:g}: {cost(r):.0f}", 10.5, "end", INK2)
    _note(c, "computed: Σ = [[1, rho], [rho, 1]], metric g = Σ⁻¹ (Section 11.1); an illustrative two-dimensional case")
    c.save(p)


def fig_11_2():
    lehman, world, loss = 0.639, 180.0, 34.0               # trillions of dollars, as the chapter states them
    assert round(100 * lehman / world, 2) == 0.35 or abs(100 * lehman / world - 0.355) < 1e-3
    ratio = loss / lehman
    assert 50 <= ratio <= 55                               # "roughly 50 times larger"
    p = reg("chapters/ch11_financial_crises.md", "11.2",
            "The three magnitudes Section 11.4 sets side by side, in trillions of dollars and as the chapter states "
            "them: the assets Lehman Brothers held in September 2008, the assets of the global financial system, and "
            "the fall in global equity values from September 2008 to March 2009. Lehman's balance sheet was about "
            "0.35% of the global one, and the fall was roughly 50 times Lehman's assets. Reading that ratio as the "
            "signature of divergent curvature is the chapter's interpretation.",
            "### Cross-Dimensional Contagion")
    c = Canvas(720, 340, "Lehman: a 0.35% perturbation and a response about 50 times larger")
    ax = Axes(c, 250, 70, 400, 180, (0, 200), (0, 3), [0, 50, 100, 150, 200], [], "trillions of dollars", "")
    for t in (50, 100, 150, 200):
        c.line(ax.X(t), ax.y0, ax.X(t), ax.y0 + ax.h, GRID, 1)
    rows = [("Lehman Brothers' assets", "the perturbation", lehman, SERIES[1], "0.639  (0.35% of the global total)"),
            ("Global equity value lost", "Sept 2008 to March 2009", loss, SERIES[1], f"34  (about {ratio:.0f} × Lehman)"),
            ("Global financial assets", "the system", world, SERIES[0], "180")]
    for i, (a, b, v, col, lab) in enumerate(rows):
        y = ax.y0 + 60 * i
        c.text(ax.x0 - 12, y + 26, a, 11.5, "end", INK)
        c.text(ax.x0 - 12, y + 41, b, 10.5, "end", INK2)
        c.hrect(ax.x0, y + 19, ax.X(v) - ax.x0, 22, col, title=f"{a}: {v} trillion")
        if v < 150:
            c.text(ax.X(v) + 8, y + 34, lab, 11, "start", INK)
        else:
            c.text(ax.X(v) - 8, y + 34, lab, 11, "end", SURFACE, "600")
    _note(c, "figures as stated in Section 11.4 of the chapter", 340)
    c.save(p)


# ------------------------------------------------------------------ chapter 12
def fig_12_1():
    d1 = {"Sofia": 100 ** 2 / 50 ** 2, "Maria": 100 ** 2 / 300 ** 2, "Crane": 100 ** 2 / 5000 ** 2}
    full = {"Sofia": 9.1, "Maria": 0.33, "Crane": 0.0004}
    assert d1["Sofia"] == 4.0 and round(d1["Maria"], 3) == 0.111 and abs(d1["Crane"] - 0.0004) < 1e-12
    assert round(d1["Sofia"] / d1["Crane"]) == 10000
    assert round(full["Sofia"] / full["Crane"]) == 22750 and round(full["Maria"] / full["Crane"]) == 825
    terms = [("d1 money", 100 ** 2 / 50 ** 2, 4.0), ("d3 fairness", 0.6 ** 2 / 0.8 ** 2, 0.5625),
             ("d4 autonomy", 0.7 ** 2 / 0.6 ** 2, 1.361), ("d9 epistemic", 0.5 ** 2 / 0.5 ** 2, 1.0),
             ("d1–d4 cross term", 2 * 0.3 * (100 / 50) * (0.7 / 0.6), 1.4)]
    for _, v, printed in terms:
        assert abs(v - printed) < 0.001 * max(1, printed) + 0.0005
    p = reg("chapters/ch12_inequality.md", "12.1",
            "The worked example of Section 12.5: the cost of one unexpected 100-dollar expense on the metrics of "
            "three agents: Sofia the barista, Maria the owner and Crane the chief executive of the REIT. Left, on a "
            "logarithmic axis, the cost on the monetary dimension alone, 100 squared over "
            "the agent's monetary scale squared, and the full-manifold cost the chapter arrives at. Right, the "
            "terms the chapter itemises for Sofia; its total of about 9.1 also includes cross terms it does not "
            "itemise. The full-manifold ratio of Sofia to Crane is 22,750 against 10,000 on money alone. " + POSITED,
            "### What the Gini Misses")
    c = Canvas(720, 400, "The same 100 dollars costs 22,750 times more on Sofia's metric")
    ax = Axes(c, 96, 96, 300, 190, (1e-4, 1e2), (0, 3), [], [], "metric cost of the 100-dollar expense (log scale)",
              "", xlog=True)
    for e in range(-4, 3):
        v = 10.0 ** e
        c.line(ax.X(v), ax.y0, ax.X(v), ax.y0 + ax.h, GRID, 1)
        c.text(ax.X(v), ax.y0 + ax.h + 16, {-4: "0.0001", -3: "0.001", -2: "0.01", -1: "0.1", 0: "1", 1: "10",
                                            2: "100"}[e], 10.5, "middle", INK2)
    who = [("Sofia", "scale 50"), ("Maria", "scale 300"), ("Crane", "scale 5,000")]
    for i, (nm, sub) in enumerate(who):
        y = ax.y0 + ax.h * (i + 0.5) / 3
        c.text(ax.x0 - 10, y, nm, 11.5, "end", INK, "600")
        c.text(ax.x0 - 10, y + 14, sub, 10, "end", INK2)
        xa, xb = ax.X(d1[nm]), ax.X(full[nm])
        if nm == "Crane":
            c.dot(xa, y, SERIES[1], 5.5, title="Crane: 0.0004 on both")
            c.dot(xa, y, SERIES[0], 3)
            c.text(xa + 12, y + 4, "0.0004 (both)", 10.5, "start", INK)
        else:
            c.line(xa, y, xb, y, INK3, 2)
            c.dot(xa, y, SERIES[0], 5, title=f"{nm}, d1 only {d1[nm]:.3g}")
            c.dot(xb, y, SERIES[1], 5, title=f"{nm}, full manifold {full[nm]}")
            c.text(xa - 9, y + 4, f"{d1[nm]:.3g}", 10.5, "end", INK)
            c.text(xb + 9, y + 4, f"{full[nm]:g}", 10.5, "start", INK)
    legend(c, 96, 76, [("d1 alone", SERIES[0]), ("full manifold", SERIES[1])], 11)
    # right panel
    ax2 = Axes(c, 470, 96, 230, 190, (0, 5), (0, 4.5), (), [0, 1, 2, 3, 4], "", "")
    c.text(470, 76, "Sofia: the itemised terms", 12, "start", INK, "600")
    labs = [("d1", "money"), ("d3", "fairness"), ("d4", "autonomy"), ("d9", "epistemic"), ("d1–d4", "cross")]
    for i, (_, v, printed) in enumerate(terms):
        x = ax2.x0 + ax2.w * (i + 0.5) / 5 - 10
        c.rect(x, ax2.Y(v), 20, ax2.Y(0) - ax2.Y(v), SERIES[1] if i else SERIES[0], title=f"{terms[i][0]} {printed}")
        c.text(x + 10, ax2.Y(v) - 6, f"{printed:g}", 10.5, "middle", INK)
        c.text(x + 10, ax2.y0 + ax2.h + 16, labs[i][0], 10.5, "middle", INK)
        c.text(x + 10, ax2.y0 + ax2.h + 30, labs[i][1], 9.5, "middle", INK2)
    c.text(585, 344, "chapter's total, with other cross terms: ≈ 9.1", 10.5, "middle", INK2)
    _note(c, "worked example of Section 12.5; scales and activations are the chapter's assumptions")
    c.save(p)


# ------------------------------------------------------------------ chapter 13
def fig_13_1():
    cost = {"A": 80 * 12, "B": 80 * 25, "C": 80 * 18}
    assert cost == {"A": 960, "B": 2000, "C": 1440}
    names = {"A": "A  commodity, Brazil", "B": "B  fair trade, via Elena", "C": "C  direct trade, Colombia"}
    price = {"A": 12, "B": 25, "C": 18}
    dims = ["d3 Fairness", "d5 Trust", "d6 Community", "d7 Identity", "d9 Epistemic"]
    vals = {"A": [-0.6, -0.3, -0.4, -0.7, None], "B": [0.5, 0.4, 0.6, 0.8, None], "C": [0.3, -0.2, None, None, -0.4]}
    assert sorted(cost, key=cost.get) == ["A", "C", "B"]   # the d1-only ranking A > C > B
    col = {"A": SERIES[1], "B": SERIES[0], "C": SERIES[2]}
    p = reg("chapters/ch13_trade.md", "13.1",
            "Maria's three sourcing options from the worked example. Left, the monthly cost of 80 pounds at each "
            "price, in dollars, with the rank on money alone. Right, the changes the chapter assigns on the other "
            "dimensions it lists for each option; a missing bar means the chapter gives no value. The chapter ranks "
            "the options B, C, A on the full manifold, the reverse of the money ranking. " + POSITED,
            "### The Conservation Laws in Maria's Trade")
    c = Canvas(720, 400, "Bean sourcing: cheapest on money, costliest on the other dimensions")
    # left
    ax1 = Axes(c, 28, 150, 196, 150, (0, 2400), (0, 3), [0, 1000, 2000], [], "dollars a month (d1)", "")
    for t in (1000, 2000):
        c.line(ax1.X(t), ax1.y0, ax1.X(t), ax1.y0 + ax1.h, GRID, 1)
    for i, k in enumerate(["A", "C", "B"]):
        y = ax1.y0 + 50 * i
        c.hrect(ax1.x0, y + 20, ax1.X(cost[k]) - ax1.x0, 20, col[k], title=f"{k}: {cost[k]} dollars a month")
        c.text(ax1.x0, y + 13, f"{['1st', '2nd', '3rd'][i]} on money: {k}, {price[k]} a pound", 10.5, "start", INK2)
        c.text(ax1.X(cost[k]) + 6, y + 34, f"{cost[k]:,}", 10.5, "start", INK)
    for i, k in enumerate("ABC"):
        c.add(f'<rect x="28" y="{50 + 22 * i}" width="12" height="12" rx="3" fill="{col[k]}"/>')
        c.text(46, 60 + 22 * i, names[k], 11.5, "start", INK)
    # right
    ax2 = Axes(c, 310, 70, 390, 250, (0, 5), (-1, 1), (), [-1, -0.5, 0, 0.5, 1], "", "")
    c.text(310, 58, "Change on the other dimensions (the chapter's scale)", 11.5, "start", INK, "600")
    base = ax2.Y(0)
    c.line(ax2.x0, base, ax2.x0 + ax2.w, base, INK3, 1)
    bw = 18
    for d in range(5):
        cx = ax2.x0 + ax2.w * (d + 0.5) / 5
        for j, k in enumerate("ABC"):
            v = vals[k][d]
            if v is None:
                continue
            x = cx - (3 * bw + 4) / 2 + j * (bw + 2)
            _vbar(c, x, base, bw, base - ax2.Y(v), col[k])
            c.text(x + bw / 2, ax2.Y(v) + (13 if v < 0 else -5), _signed(v), 9.5, "middle", INK)
        c.text(cx, ax2.y0 + ax2.h + 18, dims[d][:2], 11.5, "middle", INK)
        c.text(cx, ax2.y0 + ax2.h + 33, dims[d][3:], 10, "middle", INK2)
    c.text(505, 372, "full-manifold ranking stated in the chapter: B, then C, then A", 11, "middle", INK)
    _note(c, "worked example of Chapter 13; values assigned by the chapter, not measured")
    c.save(p)


# ------------------------------------------------------------------ chapter 14
def fig_14_1():
    panels = [
        ("1. Irreversible crossing", "β = ∞: hard cap", ["species extinction,", "aquifer depletion,", "ozone destruction"],
         "the geodesic must not cross"),
        ("2. Reversible, measurable", "β = c(social): Pigouvian tax", ["CO2 emissions, water", "pollution within", "recoverable limits"],
         "the geodesic bends in proportion"),
        ("3. Possibly irreversible", "β = c(social) + π(precaution)", ["climate tipping points,", "biodiversity loss near", "critical thresholds"],
         "the tax plus a precautionary premium"),
    ]
    p = reg("chapters/ch14_regulation.md", "14.1",
            "The three cases of Theorem 14.1 as a schematic. Each panel shows the penalty added to a path as it "
            "crosses a regulatory boundary, marked by the dashed line. An irreversible crossing gets an infinite "
            "penalty, a hard cap. A reversible crossing with a measurable cost gets a finite penalty equal to the "
            "social cost, a Pigouvian tax. A crossing that may prove irreversible gets the social cost plus a "
            "precautionary premium. Heights are not to scale.",
            "### The Tragedy of the Commons, Geometrized")
    c = Canvas(720, 400, "Three kinds of boundary, three sizes of penalty")
    pw = 216
    for i, (name, beta, ex, eff) in enumerate(panels):
        x = 18 + i * (pw + 18)
        _rect(c, x, 48, pw, 300, BOX, 1.0, 6, BORDER)
        c.add(f'<rect x="{x}" y="48" width="{pw}" height="4" rx="2" fill="{SERIES[i]}"/>')
        c.text(x + 12, 74, name, 13, "start", INK, "600")
        c.text(x + 12, 93, beta, 11.5, "start", INK)
        bx, y0 = x + 108, 236                               # boundary position, baseline
        c.line(x + 16, y0, x + pw - 16, y0, INK3, 1)
        c.line(bx, 112, bx, y0 + 6, INK2, 1.5, dash="4 4")
        c.text(x + 16, y0 + 18, "permitted", 10, "start", INK3)
        c.text(x + pw - 16, y0 + 18, "beyond the boundary", 10, "end", INK3)
        if i == 0:
            _rect(c, bx, 116, pw - 124, y0 - 116, SERIES[0], 0.35)
            c.line(bx, y0, bx, 116, SERIES[0], 3)
            c.text(bx + 46, 176, "∞", 26, "middle", INK)
            c.text(bx + 46, 196, "forbidden", 10.5, "middle", INK2)
        elif i == 1:
            _poly(c, [(x + 16, y0), (bx, y0), (bx, 190), (x + pw - 16, 190)], SERIES[1], 3)
            _rect(c, bx, 190, pw - 124, y0 - 190, SERIES[1], 0.25)
            c.text(bx + 46, 218, "c(social)", 11, "middle", INK)
        else:
            _poly(c, [(x + 16, y0), (bx, y0), (bx, 140), (x + pw - 16, 140)], SERIES[2], 3)
            _rect(c, bx, 190, pw - 124, y0 - 190, SERIES[1], 0.25)
            _rect(c, bx, 140, pw - 124, 50, SERIES[2], 0.35)
            c.line(bx, 190, x + pw - 16, 190, SERIES[1], 1.5, dash="3 3")
            c.text(bx + 46, 218, "c(social)", 11, "middle", INK)
            c.text(bx + 46, 169, "π(precaution)", 11, "middle", INK)
        c.text(x + 12, 132, "penalty", 10, "start", INK3, italic=True)
        for k, s in enumerate(ex):
            c.text(x + 12, 280 + 15 * k, s, 10.5, "start", INK2)
        c.text(x + 12, 338, eff, 10.5, "start", INK)
    _note(c, "schematic of Theorem 14.1; penalty heights are not to scale")
    c.save(p)


# ------------------------------------------------------------------ chapter 15
def fig_15_1():
    K0, al = 0.10, 0.10                                    # illustrative curvature parameters

    def hyp(t):
        return (1 + al * t) ** (-K0 / al)

    # the closed form is the exponential of minus the integral of K0 / (1 + al * tau)
    for T in (10, 50, 100):
        n = 20000
        integ = sum(K0 / (1 + al * (i + 0.5) * T / n) for i in range(n)) * T / n
        assert abs(math.exp(-integ) - hyp(T)) < 1e-6
    ts = [i * 0.5 for i in range(201)]
    p = reg("chapters/ch15_discount_rate.md", "15.1",
            "Discount functions from the formula of Section 15.4, D(t) = exp(− integral of K from 0 to t), where K "
            "is the temporal curvature. Left, the curvature: constant at the two rates Section 15.2 quotes for Stern "
            "(0.1% a year) and Nordhaus (3% a year), and declining as K0/(1 + alpha tau). Right, the discount "
            "functions these give: two exponentials, and the hyperbolic form (1 + alpha t) to the power −K0/alpha, "
            "which falls faster than the 3% exponential at first and more slowly later. The declining curve is "
            "drawn for illustrative values K0 = alpha = 0.1 a year, which the chapter does not specify.",
            "### Time-Inconsistency as Curvature Change")
    c = Canvas(720, 400, "Declining temporal curvature makes the discount function hyperbolic")
    ax1 = Axes(c, 70, 84, 240, 236, (0, 100), (0, 0.10), [0, 25, 50, 75, 100], [], "years ahead", "")
    for v in (0, 0.02, 0.04, 0.06, 0.08, 0.10):
        c.line(ax1.x0, ax1.Y(v), ax1.x0 + ax1.w, ax1.Y(v), GRID, 1)
        c.text(ax1.x0 - 8, ax1.Y(v) + 4, f"{v:.2f}", 11, "end", INK2)
    c.text(ax1.x0, 70, "Temporal curvature K (per year)", 12, "start", INK, "600")
    _poly(c, [(ax1.X(t), ax1.Y(0.001)) for t in (0, 100)], SERIES[0], 2.5)
    _poly(c, [(ax1.X(t), ax1.Y(0.03)) for t in (0, 100)], SERIES[1], 2.5)
    _poly(c, [(ax1.X(t), ax1.Y(K0 / (1 + al * t))) for t in ts], SERIES[2], 2.5)
    ax2 = Axes(c, 400, 84, 240, 236, (0, 100), (0, 1), [0, 25, 50, 75, 100], [0, 0.25, 0.5, 0.75, 1], "years ahead", "")
    c.text(ax2.x0, 70, "Discount function D(t)", 12, "start", INK, "600")
    _poly(c, [(ax2.X(t), ax2.Y(math.exp(-0.001 * t))) for t in ts], SERIES[0], 2.5)
    _poly(c, [(ax2.X(t), ax2.Y(math.exp(-0.03 * t))) for t in ts], SERIES[1], 2.5)
    _poly(c, [(ax2.X(t), ax2.Y(hyp(t))) for t in ts], SERIES[2], 2.5)
    c.text(ax2.x0 + ax2.w + 8, ax2.Y(math.exp(-0.1)) + 4, f"{math.exp(-0.1):.2f}", 10.5, "start", INK)
    c.text(ax2.x0 + ax2.w + 8, ax2.Y(hyp(100)) - 3, f"{hyp(100):.2f}", 10.5, "start", INK)
    c.text(ax2.x0 + ax2.w + 8, ax2.Y(math.exp(-3)) + 10, f"{math.exp(-3):.2f}", 10.5, "start", INK)
    legend(c, 70, 48, [("constant 0.1% (Stern)", SERIES[0]), ("constant 3% (Nordhaus)", SERIES[1]),
                       ("declining, K0/(1 + alpha tau)", SERIES[2])], 11)
    _note(c, "computed from the formula of Section 15.4; K0 = alpha = 0.1 per year is an illustrative choice")
    c.save(p)


# ------------------------------------------------------------------ chapter 16
def fig_16_1():
    p = reg("chapters/ch16_open_questions.md", "16.1",
            "The distinction on which Conjecture 16.1 turns, as a schematic. Left, two regions of the decision "
            "manifold separated by a boundary with a penalty that is high but finite: a path across exists, and a "
            "large enough offer or a clever enough instrument can take it. Right, two components with no connecting "
            "path at all: nothing can cross. Whether sacred-value boundaries are of the second kind is the open "
            "question; the chapter states it as a conjecture and it has not been tested.",
            "## 16.3 Mechanism Design on the Manifold")
    c = Canvas(720, 380, "A high wall can be crossed at a price; a disconnection cannot")

    def blob(cx, cy, rx, ry, col, label):
        c.ellipse(cx, cy, rx, ry, 0, col, col, 2, 0.14)
        c.text(cx, cy + 46, label, 11.5, "middle", INK2)

    for i, (title, sub) in enumerate((("Boundary with a finite penalty", "a regulatory rule: β large, not infinite"),
                                      ("Disconnected components", "conjectured for sacred values: no path exists"))):
        x = 18 + i * 351
        _rect(c, x, 48, 333, 284, BOX, 1.0, 6, BORDER)
        c.add(f'<rect x="{x}" y="48" width="333" height="4" rx="2" fill="{SERIES[i]}"/>')
        c.text(x + 14, 76, title, 13.5, "start", INK, "600")
        c.text(x + 14, 94, sub, 11, "start", INK2)
        blob(x + 80, 196, 58, 70, SERIES[0], "money")
        blob(x + 253, 196, 58, 70, SERIES[2], "the good")
        c.dot(x + 80, 186, INK, 4)
        c.dot(x + 253, 186, INK, 4)
        if i == 0:
            c.line(x + 166, 136, x + 166, 266, INK3, 2, dash="5 4")
            pts = [(x + 80 + (173 * t / 40), 186 - 34 * math.sin(math.pi * t / 40)) for t in range(41)]
            _poly(c, pts, CRITICAL, 2.5)
            (x1, y1), (x2, y2) = pts[-2], pts[-1]
            ang = math.atan2(y2 - y1, x2 - x1)
            for s in (+1, -1):
                c.line(x2, y2, x2 + 8 * math.cos(ang + s * 2.6), y2 + 8 * math.sin(ang + s * 2.6), CRITICAL, 2.5)
            c.text(x + 166, 126, "cost β", 11, "middle", INK)
            c.text(x + 166, 306, "a path exists: the boundary can be evaded or bought", 10.5, "middle", INK)
        else:
            c.text(x + 166, 190, "no path", 12, "middle", INK, "600")
            c.text(x + 166, 306, "no instrument can create the transition", 10.5, "middle", INK)
    _note(c, "schematic of Conjecture 16.1 (Economic No Escape); an open conjecture, not an established result", 380)
    c.save(p)
