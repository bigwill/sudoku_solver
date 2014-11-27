from model import Board
from solver import solve_board
import unittest

class SolverTestCase(unittest.TestCase):
    def _test_from_files(self, in_file_path, out_file_path):
        with open(in_file_path) as f:
            b_in = Board.FromFile(f)
        with open(out_file_path) as f:
            b_out = Board.FromFile(f)

        solve_board(b_in)

        self.assertEquals(b_in, b_out, "boards don't match (in=%s, out=%s)" % (in_file_path, out_file_path))

    def test_easy1(self):
        self._test_from_files('test_boards/easy/1.in', 'test_boards/easy/1.out')

    def test_easy2(self):
        self._test_from_files('test_boards/easy/2.in', 'test_boards/easy/2.out')

    def test_easy3(self):
        self._test_from_files('test_boards/easy/3.in', 'test_boards/easy/3.out')

    def test_easy4(self):
        self._test_from_files('test_boards/easy/4.in', 'test_boards/easy/4.out')

    def test_hard1(self):
        self._test_from_files('test_boards/hard/1.in', 'test_boards/hard/1.out')

    def test_hard2(self):
        self._test_from_files('test_boards/hard/2.in', 'test_boards/hard/2.out')

    def test_harder1(self):
        self._test_from_files('test_boards/harder/1.in', 'test_boards/harder/1.out')

    def test_harder2(self):
        self._test_from_files('test_boards/harder/2.in', 'test_boards/harder/2.out')

    def test_hardest1(self):
        self._test_from_files('test_boards/hardest/1.in', 'test_boards/hardest/1.out')
