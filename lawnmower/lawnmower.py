import sys
import unittest
from expecter import expect

class Lawn(object):
  def __init__(self, n, m, p):
    """ Create a lawn n x m meters with a pattern matrix p """
    self.n = n
    self.m = m
    self.p = p
    self.possible = [[False for col in range(self.m)] for row in range(self.n)]
  def transposed_p(self):
    """ Transpose the matrix we have for p so we can look at cols as rows """
    return [[row[i] for row in self.p] for i in range(self.m)]
  def can_it_be_done(self):
    """ Set a shadow matrix to true or false for each square's final possibilities """
    for row in range(self.n):
      max_height = max(self.p[row])
      for col in range(self.m):
        if self.p[row][col] == max_height:
          self.possible[row][col] = True
        else:
          self.possible[row][col] = False
    transposed = self.transposed_p()
    for row in range(self.m):
      max_height = max(transposed[row])
      for col in range(self.n):
        if transposed[row][col] == max_height:
          self.possible[col][row] = True or self.possible[col][row]
        else:
          self.possible[col][row] = False or self.possible[col][row]
    return min([item for sublist in self.possible for item in sublist])

class Lawns(object):
  def __init__(self, data):
    configuration = data.split('\n')
    while not configuration[0]: configuration.pop(0)
    self.count = int(configuration.pop(0))
    self.lawns = []
    for i in range(self.count):
      p = []
      (n, m) = map(lambda x: int(x), configuration.pop(0).split())
      for i in range(n):
        p.append(map(lambda x: int(x), configuration.pop(0).split()))
      self.lawns.append(Lawn(n, m, p))
  def __getitem__(self, index):
    return self.lawns[index]

def main(data):
  lawns = Lawns(data)
  i = 1
  for lawn in lawns:
    print "Case #%i: %s" % (i, "YES" if lawn.can_it_be_done() else "NO")
    i += 1

if __name__ == "__main__":
  main(sys.stdin.read())

test_data = """
4
3 3
2 1 2
1 1 1
2 1 2
5 5
2 2 2 2 2
2 1 1 1 2
2 1 2 1 2
2 1 1 1 2
2 2 2 2 2
1 3
1 2 1
2 2
1 3
5 7
"""

class TestLawn(unittest.TestCase):
  def test_lawn_init_can_count(self):
    lawns = Lawns(test_data)
    expect(lawns.count) == 4
  def test_lawns_are_present(self):
    lawns = Lawns(test_data)
    expect((lawns[0].n, lawns[0].m)) == (3,3)
    expect((lawns[2].n, lawns[2].m)) == (1,3)
  def test_lawns_have_a_pattern(self):
    lawns = Lawns(test_data)
    expect(lawns[2].p) == [[1,2,1]]
  def test_lawns_have_a_transposed_pattern(self):
    lawns = Lawns(test_data)
    expect(lawns[3].transposed_p()) == [[1,5], [3,7]]
    expect(lawns[2].transposed_p()) == [[1],[2],[1]]
  def test_whats_possible(self):
    lawns = Lawns(test_data)
    expect(lawns[0].can_it_be_done())== True
    expect(lawns[1].can_it_be_done())== False
    expect(lawns[2].can_it_be_done()) == True

