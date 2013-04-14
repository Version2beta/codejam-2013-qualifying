import sys

class Board(object):
  @classmethod
  def parse(cls, data):
    return [list(r) for r in data.split() if len(r) == 4]
  @classmethod
  def transpose(cls, board):
    return [[row[i] for row in board ] for i in range(4)]
  @classmethod
  def reverse(cls, board):
    board.reverse()
    return board
  @classmethod
  def diagonal(cls, board):
    return [c[0] for c in [board[i][i:]+board[i][:i] for i in range(4)]]
  @classmethod
  def winner(cls, row):
    if row.count('O') + row.count('T') == 4:
      return (True, "O won")
    if row.count('X') + row.count('T') == 4:
      return (True, "X won")
    if row.count('X') + row.count('O') + row.count('T') < 4:
      return (False, "Game has not completed")
    return (False, None)
  @classmethod
  def game(cls, board):
    board_transposed = Board.transpose(board)
    board_diagonal = Board.diagonal(board)
    board_alt_diagonal = Board.diagonal(Board.reverse(board))
    final = "Draw"
    for row in (
        board + board_transposed + [board_diagonal] + [board_alt_diagonal]):
      (done, outcome) = Board.winner(row)
      final = outcome or final
      if done: break
    return final

def main(data):
  cases = int(data.pop(0))
  data = "\n".join(data)
  boards = Board.parse(data)
  for i in range(cases):
    print "Case #%i: %s" % ( i+1, Board.game(boards[i*4:i*4+4]))

if __name__ == "__main__":
  main(sys.stdin.readlines())
