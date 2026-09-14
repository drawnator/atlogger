## uses decorator to create a logger that does not clutter the middle of the algorithms
## atloger
## ~ Guilherme Toledo 2026-09-12

import logging 
import logging.config
import json
import wandb

def log(attributes:list|str=None,flush=True,level=logging.INFO):
  def decorator(fn):
    def wrapper(*args, **kwargs):
      if callable(attributes) or attributes==None:
        local_attributes = fn.__name__
      else:
        local_attributes = attributes
      output = fn(*args,**kwargs)
      ATLOGGER.log(level,output,extra={"names":attributes})
      return output
    return wrapper
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
    self.run.log({record.__dict__["names"]:record.msg})
  def close(self):
    self.run.finish()
    super().close()

# with open("src/sample_config.json","r") as config_file:
#   config = json.load(config_file)
# logging.config.dictConfig(config)
ATLOGGER = logging.getLogger(f"AtLogger")
ATLOGGER.propagate = False
ATLOGGER.setLevel(logging.DEBUG)
