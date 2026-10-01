import sys
import logging
from functools import cache
from atlogger import ATLOGGER, WandbHandler, log

@log("fib")
@cache
def fibonacci(n:int):
  if n < 3: return n
  else: return fibonacci(n-1) + fibonacci(n-2)

if __name__ == "__main__":
  streamhadlr = logging.StreamHandler()
  streamhadlr.setLevel(logging.DEBUG)
  ATLOGGER.addHandler(streamhadlr)
  
  fibonacci(int(sys.argv[-1]))