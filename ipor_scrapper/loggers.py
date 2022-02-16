import sys
import logging
from loguru import logger


# Configure standard logging
class InterceptHandler(logging.Handler):
    def emit(self, record):
        # Get corresponding Loguru level if it exists
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        # Find caller from where originated the logged message
        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())


@logger.catch
def configure_logging():
    config = {
        "handlers": [
            {"sink": sys.stdout, "backtrace": True, "diagnose": True, "enqueue": False},
            {"sink": "logs.log", "backtrace": True, "diagnose": True, "enqueue": False},
        ],
        "extra": {"user": "someone"}
    }
    logger.configure(**config)
    logging.basicConfig(handlers=[InterceptHandler()], level=0)
