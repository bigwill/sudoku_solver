#!/usr/bin/env python

from model import Board
from solver import solve
import sys

def usage():
    print "%s [input board file] [expected board file]" % sys.argv[0]

def main():
    if len(sys.argv) != 3:
        usage()
        sys.exit(-1)

    with open(sys.argv[1]) as f:
        b_in = Board.FromFile(f)

    with open(sys.argv[2]) as f:
        b_expected = Board.FromFile(f)

    print 'Input:'
    print b_in
    print

    solve(b_in)

    print
    print 'Solution:'
    print b_in

    assert b_in == b_expected, 'board does not match expected result'

if __name__ == "__main__":
    main()
