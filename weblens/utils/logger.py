"""
Logging utilities for WebLens
"""
import logging
import sys
from pathlib import Path
from typing import Optional
from datetime import datetime

from rich.logging import RichHandler
from rich.console import Console

from ..config import config

# Global console instance
console = Console()


class WebLensFormatter(logging.Formatter):
    """Custom formatter for WebLens logs"""
    
    def __init__(self):
        super().__init__(
            fmt="%(asctime)s | %(name)s | %(levelname)s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
    
    def format(self, record):
        # Add extra context if available
        if hasattr(record, 'browser'):
            record.name = f"{record.name}[{record.browser}]"
        if hasattr(record, 'profile'):
            record.name = f"{record.name}[{record.profile}]"
        
        return super().format(record)


def setup_logging(level: str = "INFO", log_file: Optional[str] = None):
    """Setup logging configuration for WebLens"""
    
    # Create logs directory
    config.logs_dir.mkdir(exist_ok=True)
    
    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, level.upper()))
    
    # Clear existing handlers
    root_logger.handlers.clear()
    
    # Console handler with Rich
    console_handler = RichHandler(
        console=console,
        show_time=False,
        show_path=False,
        markup=True,
        rich_tracebacks=True
    )
    console_handler.setLevel(getattr(logging, level.upper()))
    
    # Custom formatter for console
    console_formatter = logging.Formatter("%(name)s | %(levelname)s | %(message)s")
    console_handler.setFormatter(console_formatter)
    
    root_logger.addHandler(console_handler)
    
    # File handler
    if log_file is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file = config.logs_dir / f"weblens_{timestamp}.log"
    else:
        log_file = Path(log_file)
    
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)  # Always log everything to file
    
    # Custom formatter for file
    file_formatter = WebLensFormatter()
    file_handler.setFormatter(file_formatter)
    
    root_logger.addHandler(file_handler)
    
    # Silence some noisy loggers
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    logging.getLogger("asyncio").setLevel(logging.WARNING)
    
    return log_file


def get_logger(name: str) -> logging.Logger:
    """Get a logger instance for a module"""
    return logging.getLogger(name)


class BrowserContextLogger:
    """Context manager for adding browser/profile context to logs"""
    
    def __init__(self, logger: logging.Logger, browser: str, profile: Optional[str] = None):
        self.logger = logger
        self.browser = browser
        self.profile = profile
        self.old_factory = None
    
    def __enter__(self):
        self.old_factory = logging.getLogRecordFactory()
        
        def record_factory(*args, **kwargs):
            record = self.old_factory(*args, **kwargs)
            record.browser = self.browser
            if self.profile:
                record.profile = self.profile
            return record
        
        logging.setLogRecordFactory(record_factory)
        return self.logger
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        logging.setLogRecordFactory(self.old_factory)
