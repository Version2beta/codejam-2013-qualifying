import sys
import unittest
from expecter import expect
from time import sleep

class Cases(object):
  def __init__(self, config):
    while not config[0]: config.pop(0)
    self.count = int(config.pop(0))
    self.treasures = []
    for i in range(self.count):
      chests = []
      (k, c) = map(lambda x: int(x), config.pop(0).split())
      keys = map(lambda x: int(x), config.pop(0).split())[:k]
      for l in range(c):
        chests.append(map(lambda x: int(x), config.pop(0).split()))
      self.treasures.append(Treasure(keys, chests, i + 1))
  def __getitem__(self, index):
    return self.treasures[index]

class Treasure(object):
  def __init__(self, keys, chests, num):
    self.keys = keys
    self.chests = []
    self.num = num
    i = 1
    for chest in chests:
      self.chests.append(Chest(chest, i))
      i += 1
  def __getitem__(self, index):
    return self.chests[index]
  def chests_are_open(self, chests):
    return min([c.opened for c in chests])
  def close_all_chests(self, chests):
    for c in chests:
      c.close_chest()
  def have_keys(self, keys):
    return len(keys) > 0
  def open_a_chest(self, keys, chest):
    try:
      keys.remove(chest.key)
      chest.open_chest()
      keys.extend(chest.take_keys())
      return True
    except ValueError:
      return False
  def solve(self):
    path = []
    keys = [x for x in self.keys]
    chests = [x for x in self.chests]
    done = False
    solved = False
    while not (done or solved):
      done = True
      for chest in chests:
        sleep(0.1)
        if chest.opened:
          print chest.num, "already opened"
          continue
        if self.open_a_chest(keys, chest):
          print "opened ", chest.num, keys
          path.append(chest.num)
          done = False
          if self.chests_are_open(chests):
            solved = True
            break
          if not self.have_keys(keys):
            path = []
            keys = [x for x in self.keys]
            print "ran out of keys", keys
            self.close_all_chests(chests)
            chests = [x for x in self.chests]
            continue
          break
    if solved:
      return "Case #%i: %s" % (
          self.num, " ".join((str(x) for x in path)))
    else:
      return "Case #%i: %s" % (self.num, "IMPOSSIBLE")

class Chest(object):
  def __init__(self, chest, num):
    self.key = int(chest.pop(0))
    self.num = num
    self.opened = False
    num_keys = int(chest.pop(0))
    try:
      self.keys = chest[:num_keys]
    except:
      self.keys = []
  def __getitem__(self, index):
    return self.keys[index]
  def open_chest(self):
    self.opened = True
  def take_keys(self):
    return self.keys
  def close_chest(self):
    self.opened = False


sample_input = """
3
1 4
1
1 0
1 2 1 3
2 0
3 1 2
3 3
1 1 1
1 0
1 0
1 0
1 1
2
1 1 1
"""

def main(config):
  treasures = Cases(config)
  for treasure in treasures:
    print treasure.solve()

if __name__ == "__main__":
  main(sys.stdin.readlines())

class TestConfiguration(unittest.TestCase):
  def test_can_count_test_cases(self):
    t = Cases(sample_input.split("\n"))
    expect(t.count) == 3
  def test_can_make_treasures(self):
    t = Cases(sample_input.split("\n"))
    expect(t[0].chests[1].keys) == [1, 3]
    expect(t[2].chests[0].keys) == [1]
  def test_that_we_start_with_the_right_keys(self):
    t = Cases(sample_input.split("\n"))
    expect(t[0].keys) == [1]

class TestKeysAndChests(unittest.TestCase):
  def test_that_some_chests_are_unopened(self):
    t = Cases(sample_input.split("\n"))
    expect(t[0].chests_are_open(t[0].chests)) == False
  def test_that_all_chests_are_opened(self):
    t = Cases(sample_input.split("\n"))
    for chest in t[0]:
      chest.open_chest()
    expect(t[0].chests_are_open(t[0].chests)) == True
    for chest in t[0]:
      chest.close_chest()
    expect(t[0].chests_are_open(t[0].chests)) == False
  def test_that_there_are_keys_left(self):
    t = Cases(sample_input.split("\n"))
    expect(t[0].have_keys(t[0].keys)) == True
  def test_that_keys_are_all_used(self):
    t = Cases(sample_input.split("\n"))
    t[0].keys = []
    expect(t[0].have_keys(t[0].keys)) == False
  def test_that_we_consume_keys(self):
    t = Cases(sample_input.split("\n"))
    t[0].open_a_chest(t[0].keys, t[0].chests[0])
    expect(t[0].have_keys(t[0].keys)) == False
  def test_that_we_can_get_keys(self):
    t = Cases(sample_input.split("\n"))
    t[0].open_a_chest(t[0].keys, t[0].chests[1])
    expect(t[0].keys) == [1,3]

class TestSolvingATreasure(unittest.TestCase):
  def test_solving_a_treasure(self):
    t = Cases(sample_input.split("\n"))
    expect(t[0].solve()) == "Case #1: 2 1 4 3"
