import os
import sys
import numpy as np

def is_p(x):
  return str(x) == str(x)[::-1]

def genroots():
  for i in range(1,100):
    if is_p(i):
      yield i
  x = 3
  while x < 10**24:
    ys = np.base_repr(x,3)
    yield np.int(ys+ys[:-1][::-1])
    yield np.int(ys+ys[::-1])
    x += 1

def write_fairsquares_to_disk(filename):
  with open(filename, "w") as fh:
    last_result = 0
    while len(str(last_result)) <= 99:
      for y in genroots():
        y2 = np.square(y)
        if is_p(y2):
          fh.write("%s,%s\n" % (str(y),str(y2)))
          last_result = y2

def main(data):
  if not os.path.exists("fairsquares.txt"):
    write_fairsquares_to_disk("fairsquares.txt")
  #fairsquares = 
  while not data[0]: data.pop(0)
  count = int(data.pop(0))
  for i in range(count):
    print "Case #%i: %i" % (i+1, 0)


if __name__ == "__main__":
  main(sys.stdin.readlines())
