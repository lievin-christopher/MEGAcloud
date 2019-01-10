import logging
import logging.handlers

class Logger(logging.Logger):
    def __init__(self,log_file="mega_activity.log"):
        self.logger = logging.getLogger()
        formatter = logging.Formatter('%(asctime)s :: %(levelname)s :: %(message)s')
        file_handler = logging.handlers.RotatingFileHandler('mega_activity.log', 'a', 1000000, 1)
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)
        self.logger.setLevel(0)

