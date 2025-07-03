import logging
import os

class Log:
    def __init__(self, log_dir:str, logger_name:str, task_id:str):
        self.logger = logging.getLogger(logger_name) # Creates or gets the logger
        self.logger.setLevel(logging.INFO) #  will capture .info(), .warning(), .error() etc. but not .debug().
        path = os.path.join(log_dir, "logs", f"{task_id}.log")
        os.makedirs(os.path.join(log_dir, "logs"), exist_ok=True)
        file_handler = logging.FileHandler(filename=path, mode="w")
        file_handler.setFormatter(logging.Formatter(
        '%(asctime)s | %(levelname)s | %(threadName)s | %(name)s | %(filename)s:%(lineno)d | %(message)s')
        )  #
        self.logger.addHandler(file_handler)
    
    def addInfo(self, msg:str):
        self.logger.info(msg)
    
    def addError(self, msg:str):
        self.logger.error(msg)
    
    def addWarning(self, msg:str):
        self.logger.warning(msg)
    
