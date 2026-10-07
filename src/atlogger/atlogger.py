## uses decorator to create a logger that does not clutter the middle of the algorithms
## atloger
## ~ Guilherme Toledo 2026-09-12

import logging 
import logging.config
import json

logger = logging.getLogger(f"AtLogger")
logger.propagate = False
logger.setLevel(logging.DEBUG)

PROD = logging.CRITICAL #50
STAGE = logging.ERROR #40
TEST = logging.WARNING #30
DEV = logging.INFO #20
DEBUG = logging.DEBUG #10
NOTSET = logging.NOTSET #0

def log(*logargs,level=logging.INFO,flush=True,**logkwargs):
  """decorator that connects with the handlers provided to log the output of a function
  Args:
    *logargs: positional arguments used no name each output of the target function
    level: log level, can be used interchangeably with python default library logging enum 
          however the ones in this  package have names better fitting for this context 
    flush: not implemented yet
  """
  def decorator(fn):
    def wrapper(*args, **kwargs):
      if (len(logargs) > 0 and callable(logargs[0])) or (len(logargs) == 0):
        local_attributes = fn.__name__
      else:
        local_attributes = logargs
      output = fn(*args,**kwargs)
      logger.log(level,output,extra={"_ATLOGGER_VARIABLENAME":local_attributes,"kwargs":kwargs})
      return output
    return wrapper

  if len(logargs) > 0 and callable(logargs[0]):
    return decorator(logargs[0])
  return decorator


# with open("src/sample_config.json","r") as config_file:
#   config = json.load(config_file)
# logging.config.dictConfig(config)