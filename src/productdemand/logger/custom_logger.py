import os
import logging
from datetime import datetime
import structlog


class CustomLogger:
    def __init__(self, log_dir: str = "logs"):

        self.log_dir = os.path.join(os.getcwd(), log_dir)
        os.makedirs(self.log_dir, exist_ok=True)

        log_file = datetime.now().strftime("%Y_%m_%d_%H_%M_%S.log")
        self.log_file_path = os.path.join(self.log_dir, log_file)

        self._configure_logging()

    def _configure_logging(self):

        file_handler = logging.FileHandler(self.log_file_path)
        console_handler = logging.StreamHandler()

        formatter = logging.Formatter("%(message)s")

        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        logging.basicConfig(
            level=logging.INFO,
            handlers=[console_handler, file_handler],
        )

        structlog.configure(
            processors=[
                structlog.processors.TimeStamper(fmt="iso", utc=True),
                structlog.processors.add_log_level,
                structlog.processors.EventRenamer("event"),
                structlog.processors.JSONRenderer(),
            ],
            logger_factory=structlog.stdlib.LoggerFactory(),
            cache_logger_on_first_use=True,
        )

    def get_logger(self, name: str):
        return structlog.get_logger(name)


_logger = CustomLogger()


def get_logger(name: str):
    return _logger.get_logger(name)
