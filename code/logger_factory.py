# code/logger_factory.py
import logging
import logging.config
import yaml
import os

#Create private SmartLogger wrapper class that optimizes the logging by only calling if the yaml
#is set to that level or above. Stacklevel is set to 2 to ensure the original call's file will be
#output and not the wrapper.
class _SmartLogger:
    def __init__(self, name):
        self._logger = logging.getLogger(name)

    def debug(self, msg, *args, **kwargs):
        if self._logger.isEnabledFor(logging.DEBUG):
            self._logger.debug(msg, *args, stacklevel = 2, **kwargs)

    def info(self, msg, *args, **kwargs):
        if self._logger.isEnabledFor(logging.INFO):
            self._logger.info(msg, *args, stacklevel = 2, **kwargs)

    def warning(self, msg, *args, **kwargs):
        if self._logger.isEnabledFor(logging.WARNING):
            self._logger.warning(msg, *args, stacklevel = 2, **kwargs)

    def error(self, msg, *args, **kwargs):
        if self._logger.isEnabledFor(logging.ERROR):
            self._logger.error(msg, *args, stacklevel = 2, **kwargs)

    def critical(self, msg, *args, **kwargs):
        self._logger.critical(msg, *args, stacklevel = 2, **kwargs)

    #Allows traceback
    def exception(self, msg, *args, **kwargs):
        self._logger.exception(msg, *args, stacklevel = 2, **kwargs)

#Create singleton Logger factory to ensure only one Logger is allocated.
class LoggerFactory:
    _initialized = False
    _general_logger = None
    _security_logger = None

    @staticmethod
    def initialize():
        if LoggerFactory._initialized:
            return
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        config_path = os.path.join(base_dir, 'configs', 'logging_config.yaml')
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
            logging.config.dictConfig(config)
        LoggerFactory._initialized = True

    @staticmethod
    def get_general_logger() -> logging.Logger:
        LoggerFactory.initialize()
        if LoggerFactory._general_logger is None:
            LoggerFactory._general_logger = _SmartLogger("generalLogger")
        return LoggerFactory._general_logger

    @staticmethod
    def get_security_logger() -> logging.Logger:
        LoggerFactory.initialize()
        if LoggerFactory._security_logger is None:
            LoggerFactory._security_logger = _SmartLogger("securityLogger")
        return LoggerFactory._security_logger
