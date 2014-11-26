#!/usr/bin/env python

from model import Board
import sys

def solve_cell(cell):
    if cell.get_v():
        return False

    possibles = cell.possible_vs()
    if len(possibles) == 1:
        cell.set_v(possibles.pop())
        return True
    else:
        return False

def solve_constraint(cons):
    solved = False
    for v in cons.unused_values.copy():
        v_cells = set()
        for cell in cons.get_cells():
            if v in cell.possible_vs():
                v_cells.add(cell)
        if len(v_cells) == 1:
            v_cells.pop().set_v(v)
            solved = True
    return solved

def solve(b):
    progress = True
    while progress:
        progress = False

        for cell in b.get_cells():
            if solve_cell(cell):
                progress = True

        for cons in b.get_constraints():
            if solve_constraint(cons):
                progress = True

        if b.is_solved():
            return

def main():
    b = Board.FromFile(sys.stdin)

    print 'Input:'
    print b
    print

    solve(b)

    print
    print 'Solution:'
    print b

if __name__ == "__main__":
    main()
