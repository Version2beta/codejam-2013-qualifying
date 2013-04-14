import unittest
from expecter import expect
from tttt import Board, main

testdata_small = """
6
XXXT
....
OO..
....

XOXT
XXOO
OXOX
XXOO

XOX.
OX..
....
....

OOXX
OXXX
OX.T
O..O

XXXO
..O.
.O..
T...

OXXX
XO..
..O.
...O
"""

testdata_xwon = """
XXXT
....
OO..
....
"""

testdata_draw = """
XOXT
XXOO
OXOX
XXOO
"""

testdata_incomplete = """
XOX.
OX..
....
....
"""

testdata_owonv = """
OOXX
OXXX
OX.T
O..O
"""

testdata_owondr = """
XXXO
..O.
.O..
T...
"""

testdata_owondl = """
OXXX
XO..
..O.
...O
"""

class TestTTTT(unittest.TestCase):
  def test_parsing_data(self):
    expect(Board.parse(testdata_xwon)) == \
      [['X', 'X', 'X', 'T'],['.', '.', '.', '.'],\
       ['O', 'O', '.', '.'],['.', '.', '.', '.']]
  def test_reversing_data(self):
    b = Board.parse(testdata_owondr)
    expect(Board.reverse(b)) == \
      [['T', '.', '.', '.'],['.', 'O', '.', '.'],\
       ['.', '.', 'O', '.'],['X', 'X', 'X', 'O']]
  def test_transposing_data(self):
    b = Board.parse(testdata_xwon)
    expect(Board.transpose(b)) == \
      [['X', '.', 'O', '.'],['X', '.', 'O', '.'],\
       ['X', '.', '.', '.'],['T', '.', '.', '.']]
  def test_diagonal_data(self):
    b = Board.parse(testdata_owondl)
    expect(Board.diagonal(b)) == ['O', 'O', 'O', 'O']
  def test_alt_diagonal_data(self):
    b = Board.reverse(Board.parse(testdata_owondr))
    expect(Board.diagonal(b)) == ['T', 'O', 'O', 'O']
  def test_winning_row(self):
    expect(Board.winner(['T', 'O', 'O', 'O'])) == (True, "O won")
    expect(Board.winner(['X', 'X', 'X', 'X'])) == (True, "X won")
  def test_games(self):
    expect(Board.game(Board.parse(testdata_xwon))) == "X won"
    expect(Board.game(Board.parse(testdata_draw))) == "Draw"
    expect(Board.game(Board.parse(testdata_incomplete))) == "Game has not completed"
    expect(Board.game(Board.parse(testdata_owonv))) == "O won"
    expect(Board.game(Board.parse(testdata_owondr))) == "O won"
    expect(Board.game(Board.parse(testdata_owondl))) == "O won"

