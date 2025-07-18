"""Logger module for the llm-chatbot-services"""
import logging
import os
import sys

class Logger:
    """Logger class for the llm-chatbot-services"""
    def __init__(self, name: str = "llm-chatbot") -> None:
        self.logger = logging.getLogger(name)
        self.set_log_level()
        self.add_handler()

    def set_log_level(self) -> None:
        """Set the log level from the environment"""
        log_level = os.getenv("LOG_LEVEL", "INFO").upper()
        self.logger.setLevel(getattr(logging, log_level, logging.INFO))

    def add_handler(self) -> None:
        """Add a handler to the logger"""
        if not self.logger.handlers:
            handler = logging.StreamHandler(sys.stdout)
            formatter = logging.Formatter(
                "[%(asctime)s] [%(levelname)s] %(name)s: %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S"
            )
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)

    def get_logger(self) -> logging.Logger:
        return self.logger

def get_logger(name: str = "llm-chatbot") -> logging.Logger:
    logger = logging.getLogger(name)

    # Set log level from environment
    log_level = os.getenv("LOG_LEVEL", "INFO").upper()
    logger.setLevel(getattr(logging, log_level, logging.INFO))

    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter(
            "[%(asctime)s] [%(levelname)s] %(name)s: %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger
