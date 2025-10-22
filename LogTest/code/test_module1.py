# code/app_module.py
from logger_factory import LoggerFactory

def run_app_logic():
    logger = LoggerFactory.get_general_logger()
    logger.warning("Running app logic")
    logger.info("App logic completed")

if __name__ == "__main__":
    run_app_logic()