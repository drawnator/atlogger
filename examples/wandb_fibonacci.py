from atlogger import ATLOGGER, WandbHandler
from fibonacci import fibonacci
import sys

if __name__ == "__main__":
  ATLOGGER.addHandler(
    WandbHandler(
      project="your_project_name",
      config={"config":True},
      level="DEBUG"
      )
  )
  fibonacci(int(sys.argv[-1]))