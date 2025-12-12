"""
Logging utilities for the agent.
"""

import logging
from pathlib import Path
from logging.handlers import RotatingFileHandler

def setup_logging(log_dir: str = "logs", log_level=logging.INFO) -> None:
    """
    Set up logging configuration for the entire application.
    
    Args:
        log_dir: Directory to store log files
        log_level: Logging level
    """
    Path(log_dir).mkdir(parents=True, exist_ok=True)
    
    # Create logger
    logger = logging.getLogger()
    logger.setLevel(log_level)
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)
    console_format = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    console_handler.setFormatter(console_format)
    
    # File handler
    log_file = Path(log_dir) / "agent.log"
    file_handler = RotatingFileHandler(
        log_file,
        maxBytes=10485760,  # 10MB
        backupCount=5
    )
    file_handler.setLevel(log_level)
    file_handler.setFormatter(console_format)
    
    # Add handlers
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
