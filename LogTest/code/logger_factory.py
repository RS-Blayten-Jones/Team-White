# code/logger_factory.py
import logging
import logging.config
import yaml
import os

class LoggerFactory:
    _general_logger = None
    _security_logger = None
    _initialized = False

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
    def get_general_logger():
        LoggerFactory.initialize()
        if LoggerFactory._general_logger is None:
            LoggerFactory._general_logger = logging.getLogger('generalLogger')
        return LoggerFactory._general_logger

    @staticmethod
    def get_security_logger():
        LoggerFactory.initialize()
        if LoggerFactory._security_logger is None:
            LoggerFactory._security_logger = logging.getLogger('securityLogger')
        return LoggerFactory._security_logger