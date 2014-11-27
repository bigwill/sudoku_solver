#!/usr/bin/env python

from model import Board
from solver import solve_board
import sys

def usage():
    print "%s [input board file] [expected board file]" % sys.argv[0]

def main():
    if not 2 <= len(sys.argv) <= 3:
        usage()
        sys.exit(-1)

    with open(sys.argv[1]) as f:
        b_in = Board.FromFile(f)

    if len(sys.argv) == 3:
        with open(sys.argv[2]) as f:
            b_exp = Board.FromFile(f)
    else:
        b_exp = None

    print '\nInput:\n\n', b_in, '\n'

    solve_board(b_in)

    print '\nSolution:\n\n', b_in, '\n'

    if b_exp:
        assert b_in == b_exp, 'board does not match expected result'

if __name__ == "__main__":
    main()
