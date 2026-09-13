# atlogger
Python decorator to log artifacts with mlflow, wandb 

Inspired by the talks with colleagues, frustrating nights and the [python logging documentation](https://docs.python.org/3/howto/logging-cookbook.html) I am attempting to develop a module to streamline the proper logging for model training and comparisons

# How to use
```bash
export WANDB_API_KEY="wandb_key"
```
```python
# main.py
from atlogger import ATLOGGER, WandbHandler

ATLOGGER.addHandler(
    WandbHandler(
      project="your_project_name",
      config={"config":True},
      level="DEBUG"
      )
  )
```
```python
# lossFunc.py
from atlogger import log

@log
loss(x1,x2):
  return abs(x1 - x2)

@log("euclidean distance")
calc_distance(x1,x2):
  return sqrt(x1**2 - x2**2)
```
# Principles 
Ideally this project will have the following principles:
* Non-intrusive:
  * Snippets used for logging shouldn't be in the middle of the code. Anyone should be able to import code from one project to another without having to go through and delete or change lines throughout the functions.
* Modular:
  * Added visualizations should be easy to add and be defined on their own and reused anywhere needed.
* Explicit:
  * Logging shall not happen under the hood. you should be able to define and easily recognize when information is being logged but also have sensible defaults as not to loose important information that is constantly ignored (i.e. logging hardware load during ML models training)
* Adaptable:
  * I want to be able to use this tool for logging diverse kinds of code and easily change between them:
    1. Ml training
    2. Compression algorithms
    3. async algorithms

# Known bugs
* if you use the decorator as @log instead of @log()the function will be passed as the variable "names" for some reason
* Curently not accepting multiple outputs from functions
* Creating the wandbhandler with config file for some reason does not get to this part of the login```wandb: Currently logged in as: <usr> to https://api.wandb.ai. Use `wandb login --relogin` to force relogin```