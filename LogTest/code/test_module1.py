# code/test_module1.py
from logger_factory import LoggerFactory
from test_module2 import check_access

def run_app_logic():
    logger = LoggerFactory.get_general_logger()
    logger.info("Testing 1.1")
    logger.info("Testing 1.2")
    try:
        1 / 0
    except Exception:
        logger.exception("Division failed")

if __name__ == "__main__":
    run_app_logic()
    check_access("employee")
    check_access("admin")