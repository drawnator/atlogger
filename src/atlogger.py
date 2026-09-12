## uses decorator to create a logger that does not clutter the middle of the algorithms
## atloger
## ~ Guilherme Toledo 2026-09-12

import logging 
import logging.config
from dataclasses import dataclass
import json

def log(fn,level=logging.INFO):
  # do something when importing fn with decorator
  def wrapper(*args, **kwargs):
    # do something before calling fn
    output = fn(*args,**kwargs)
    match level:
      case logging.DEBUG:
        ATLOGGER.debug(output)
      case logging.INFO:
        ATLOGGER.info(output)
      case logging.WARN:
        ATLOGGER.warn(output)
      case logging.ERROR:
        ATLOGGER.error(output)
      case logging.CRITICAL:
        ATLOGGER.critical(output)
    return output
  return wrapper

class MlflowHandler(logging.Handler):
  def __init__(self,*args,**kwargs):
    logging.Handler.__init__(self)
  def emit(self,record):
    pass

class WandbHandler(logging.Handler):
  def __init__(self,*args,**kwargs):
    logging.Handler.__init__(self)
  def emit(self,record):
    pass

with open("src/sample_config.json","r") as config_file:
  config = json.load(config_file)
logging.config.dictConfig(config)
ATLOGGER = logging.getLogger(f"AtLogger")