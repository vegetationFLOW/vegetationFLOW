import logging
import os

class Log:
    def __init__(self, logger_name:str, task_id:str):
        self.logger = logging.getLogger(logger_name) # Creates or gets the logger
        self.logger.setLevel(logging.INFO) #  will capture .info(), .warning(), .error() etc. but not .debug().
        path = os.path.join(os.getcwd(), "vegetationFLOW_core", "logs", f"{task_id}.log")
        file_handler = logging.FileHandler(filename=path)
        file_handler.setFormatter(logging.Formatter('%(asctime)s - %(message)s'))  #
        self.logger.addHandler(file_handler)
    
    def addInfo(self, msg:str):
        self.logger.info(msg)
    
    def addError(self, msg:str):
        self.logger.error(msg)
    
    def addWarning(self, msg:str):
        self.logger.warning(msg)
    
