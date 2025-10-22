# security_module.py
from logger_factory import LoggerFactory

def check_access(user_role):
    security_logger = LoggerFactory.get_security_logger()
    security_logger.warning(f"Access check initiated for role: {user_role}")

    if user_role != "admin":
        security_logger.warning(f"Unauthorized access attempt by role: {user_role}")
    else:
        security_logger.info("Admin access granted.")

if __name__ == "__main__":
    LoggerFactory.initialize()  # Make sure config is loaded
    check_access("Admin")