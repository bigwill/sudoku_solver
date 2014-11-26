#!/usr/bin/env python

import sys

class Board(object):
    @staticmethod
    def FromFile(f):
        b = Board()

        y = 0
        for l in f.xreadlines():
            l = l.rstrip()
            assert len(l) == 9, 'expected 9 characters per line'

            for (x, v) in enumerate(l):
                if v in '_':
                    continue
                v = int(v)
                assert 1 <= v <= 9, 'invalid v encountered: %d' % v
                b.get_cell(x, y).set_v(v)
            y += 1
        assert y == 9, 'expected 9 lines of input'

        return b

    def __init__(self):
        # create cells
        self.cells = set()
        self.cells_map = {}

        for i in xrange(0, 9):
            self.cells_map[i] = {}
            for j in xrange(0, 9):
                cell = Cell((i, j))
                self.cells_map[i][j] = cell
                self.cells.add(cell)

        assert len(self.cells) == 81, 'Expected 81 cells, found %d' % len(self.cells)

        # create constraints
        self.constraints = set()

        ## row constraints
        for i in xrange(0, 9):
            self.constraints.add(Constraint((cell for cell in self.cells if cell.x == i)))

        ## column constraints
        for i in xrange(0, 9):
            self.constraints.add(Constraint((cell for cell in self.cells if cell.y == i)))

        ## box constraints
        boxes = [((0, 0), (3, 3)),
                 ((3, 0), (6, 3)),
                 ((6, 0), (9, 3)),
                 ((0, 3), (3, 6)),
                 ((0, 6), (3, 9)),
                 ((3, 3), (6, 6)),
                 ((3, 6), (6, 9)),
                 ((6, 3), (9, 6)),
                 ((6, 6), (9, 9))]
        for ((xl, yl), (xu, yu)) in boxes:
            self.constraints.add(Constraint((cell for cell in self.cells if xl <= cell.x < xu and yl <= cell.y < yu)))

        assert len(self.constraints) == 27, 'Expected 27 constraints, found %d' % len(self.constraints)

    def get_cell(self, x, y):
        return self.cells_map[x][y]

    def get_constraints(self):
        return self.constraints.copy()

    def verify(self):
        return all(cons.verify() for cons in self.constraints)

    def __str__(self):
        ls = []
        for y in xrange(0, 9):
            vs = (self.get_cell(x, y).get_v() for x in xrange(0, 9))
            vps = (str(v) if v else '_' for v in vs)
            ls.append(''.join(vps))
        return '\n'.join(ls)

class Cell(object):
    def __init__(self, p, v=None):
        self.x = p[0]
        self.y = p[1]
        self.v = v
        self.constraints = set()

    # Cells and constraints become related via the _add_cell(..) method on Constraint.
    def _add_constraint(self, cons):
        assert cons.contains_cell(self), 'A cell cannot add a constraint to which it is not a member'
        self.constraints.add(cons)

    def possible_vs(self):
        possible = set(xrange(1, 10))
        for cons in self.constraints:
            possible.intersection_update(cons.unused_values)
        return possible

    def set_v(self, v):
        assert v is None or v in self.possible_vs(), 'Cannot set v to %d, it does not satisfy constraints at pos (%d, %d)' % (v, self.x, self.y)
        old_v = self.v
        self.v = v
        for cons in self.constraints:
            cons._cell_modified(self, old_v)

    def get_v(self):
        return self.v

    def crank(self):
        if self.get_v():
            return False

        possibles = self.possible_vs()
        if len(possibles) == 1:
            self.set_v(possibles.pop())
            return True
        else:
            return False

class Constraint(object):
    def __init__(self, cells):
        self.unused_values = set(xrange(1, 10))
        self.cells = set()
        for cell in cells:
            self._add_cell(cell)
        assert len(self.cells) == 9, 'Expected exactly 9 cells in constraint group, got %d' % len(self.cells)

    def contains_cell(self, cell):
        return cell in self.cells

    def verify(self):
        used_values = set()
        for cell in self.cells:
            v = cell.get_v()
            if v is not None:
                used_values.add(v)
        return sum(used_values) + sum(self.unused_values) == sum(xrange(1, 10))

    def _add_cell(self, cell):
        if not self.contains_cell(cell):
            self.cells.add(cell)
            cell._add_constraint(self)

    def _cell_modified(self, cell, old_v):
        assert cell.v in self.unused_values, 'Cell set to value %d, but that is not allowed by this constraint' % cell.v
        self.unused_values.remove(cell.v)
        if old_v is not None:
            self.unused_values.add(old_v)

    def crank(self):
        solved = False
        for v in self.unused_values.copy():
            v_cells = set()
            for cell in self.cells:
                if v in cell.possible_vs():
                    v_cells.add(cell)
            if len(v_cells) == 1:
                v_cells.pop().set_v(v)
                solved = True
        return solved

def main():
    b = Board.FromFile(sys.stdin)

    print 'Input:'
    print b
    print

    crank_worked = True
    while crank_worked:
        crank_worked = False

        for x in xrange(0, 9):
            for y in xrange(0, 9):
                if b.get_cell(x, y).crank():
                    crank_worked = True

        for cons in b.get_constraints():
            if cons.crank():
                crank_worked = True

        # are we done?
        done = True
        for x in xrange(0, 9):
            for y in xrange(0, 9):
                if b.get_cell(x, y).get_v() is None:
                    done = False

        if done:
            break

    print
    print 'Solution:'
    print b
    assert b.verify(), 'Board b did not pass constraints'

if __name__ == "__main__":
    main()
