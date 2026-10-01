import sys
import logging
from functools import cache
from atlogger import ATLOGGER, WandbHandler, log

@log("factorial",level=logging.WARN)
def factorial(n:int):
  if n < 3:
    return n
  else:
    return n * factorial(n-1)

if __name__ == "__main__":
  streamhadlr = logging.StreamHandler()
  streamhadlr.setLevel(logging.WARN)
  ATLOGGER.addHandler(streamhadlr)

  factorial(int(sys.argv[-1]))