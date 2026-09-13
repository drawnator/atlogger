from functools import cache
from atlogger import log

@log("n")
@cache
def fibonacci(n:int):
  if n < 3: return n
  else: return fibonacci(n-1) + fibonacci(n-2)
