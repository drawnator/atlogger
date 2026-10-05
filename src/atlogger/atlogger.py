## uses decorator to create a logger that does not clutter the middle of the algorithms
## atloger
## ~ Guilherme Toledo 2026-09-12

import logging 
import logging.config
import json
import wandb

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

class MlflowHandler(logging.Handler):
  def __init__(self,*args,**kwargs):
    logging.Handler.__init__(self,**kwargs)
    import mlflow
    print("init MlflowHandler")
  def emit(self,record):
    pass

class WandbHandler(logging.Handler):
  run:wandb.Run=None
  def __init__(self,
  *args,
  project:str="unamed_project",
  config:dict={},
  run:wandb.Run=None,
  **kwargs):
    logging.Handler.__init__(self,**kwargs)
    wandb.login()
    if run is not None:
      self.run = run
    else:
      self.run = wandb.init(project=project,config=config)
    
  def emit(self,record):
    variable_name = record.__dict__["_ATLOGGER_VARIABLENAME"]
    if len(variable_name) == record.msg:
      print("equal")
      output = dict(zip(variable_name,record.msg))
      #TODO add to run.log
    self.run.log({record.__dict__["_ATLOGGER_VARIABLENAME"]:record.msg})#,**record.__dict__["kwargs"])
  def close(self):
    self.run.finish()
    super().close()

# with open("src/sample_config.json","r") as config_file:
#   config = json.load(config_file)
# logging.config.dictConfig(config)