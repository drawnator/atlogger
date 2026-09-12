## documentation
## atloger
## ~ Guilherme Toledo 2026-09-12

def log(fn):
  # do something when importing fn with decorator
  print(f"logging: {fn.__module__}:{fn.__name__}")
  def wrapper(*args, **kwargs):
    # do something before calling fn
    output = fn(*args,**kwargs)
    # do something after calling fn
    print(output)
    return output
  return wrapper
