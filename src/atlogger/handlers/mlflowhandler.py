import logging 
import mlflow

class MlflowHandler(logging.Handler):
  def __init__(self,*args,**kwargs):
    logging.Handler.__init__(self,**kwargs)
    print("init MlflowHandler")
  def emit(self,record):
    pass