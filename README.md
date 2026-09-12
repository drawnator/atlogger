# atlog
Python decorator to log artifacts with mlflow, wandb 

Inspired by the talks with colleagues, frustrating nights and the [python logging documentation](https://docs.python.org/3/howto/logging-cookbook.html) I am attempting to develop a module to streamline the proper logging for model training and comparisons

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