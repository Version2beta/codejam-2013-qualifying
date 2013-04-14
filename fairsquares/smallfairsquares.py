import os
import sys
import numpy as np
import pandas as pd

def is_p(x):
  return str(x) == str(x)[::-1]

def genroots():
  x = 1
  while x < 10**7:
    if is_p(x):
      yield x
    x += 1

def fairsquares():
  return [y*y for y in genroots() if is_p(y*y)]

def main(data):
  while not data[0]: data.pop(0)
  count = int(data.pop(0))
  sq = pd.Series(fairsquares())
  for i in range(count):
    (lowest, highest) = data.pop(0).split()
    print "Case #%i:" % (i+1),
    print len(sq[(sq >= int(lowest)) & (sq <= int(highest))])


if __name__ == "__main__":
  main(sys.stdin.readlines())
