import logging

class PyXBRLToolsLogging(object):
    """ PyXBRLToolsのログ設定クラス。"""
    def __init__(self, log_level=logging.INFO):
        self.logger = logging.getLogger('PyXBRLTools')
        self.logger.setLevel(log_level)
        self.log_level = log_level
        self.log_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.log_console_handler = logging.StreamHandler()
        self.log_console_handler.setFormatter(self.log_format)
        self.logger.addHandler(self.log_console_handler)
        self.log_file_handler = None

    def set_log_file(self, log_file):
        self.log_file_handler = logging.FileHandler(log_file)
        self.log_file_handler.setFormatter(self.log_format)
        self.logger.addHandler(self.log_file_handler)

    def set_log_level(self, log_level):
        self.logger.setLevel(log_level)
        self.log_level

