"""Parse the Post et al. (2008) Deal or No Deal workbook into states and decisions.

    python parse_post.py 20060455_Data.xls states.tsv decisions.tsv

States and decisions go to separate files so that a held-out set parsed the same
way can have its states read without its decisions. Names are not written.

states.tsv:    id, sheet, round, offer, remaining prizes (space separated), full board (space separated)
decisions.tsv: id, round, decision (D or ND)
"""
import sys

import xlrd

FIRST_PRIZE_COL = 11        # columns from here on are prizes, amounts in the header row


def main(xls, states_out, decisions_out):
    book = xlrd.open_workbook(xls)
    n = 0
    with open(states_out, "w") as fs, open(decisions_out, "w") as fd:
        for sh in book.sheets():
            head = [sh.cell_value(0, c) for c in range(sh.ncols)]
            col = {str(h): i for i, h in enumerate(head)}
            prizes = [float(h) for h in head[FIRST_PRIZE_COL:]]
            for r in range(1, sh.nrows):
                cid = sh.cell_value(r, col["ID Number"])
                rnd = sh.cell_value(r, col["ROUND"])
                if cid == "" or rnd == "":
                    # The USX sheet repeats a header row before each contestant, with that
                    # contestant's own prize board. Take the board from it.
                    cells = [sh.cell_value(r, c) for c in range(FIRST_PRIZE_COL, sh.ncols)]
                    if all(isinstance(v, float) for v in cells):
                        prizes = cells
                    continue
                cid = str(int(cid)) if isinstance(cid, float) else str(cid)
                left = [p for p, c in zip(prizes, range(FIRST_PRIZE_COL, sh.ncols))
                        if sh.cell_value(r, c) == 1]
                fs.write("\t".join([cid, sh.name, str(int(rnd)), repr(float(sh.cell_value(r, col["Bank Offer"]))),
                                    " ".join(repr(p) for p in left), " ".join(repr(p) for p in prizes)]) + "\n")
                fd.write("\t".join([cid, str(int(rnd)), str(sh.cell_value(r, col["Deal / No Deal"])).strip()]) + "\n")
                n += 1
    print("rows", n)


if __name__ == "__main__":
    main(*sys.argv[1:4])
