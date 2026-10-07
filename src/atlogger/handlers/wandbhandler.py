import logging
import wandb

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