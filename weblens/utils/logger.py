"""
Logging utilities for WebLens
"""
import logging
import sys
from pathlib import Path
from typing import Optional, Any
from datetime import datetime

from rich.logging import RichHandler
from rich.console import Console

from ..config import config


class WebLensLogRecord(logging.LogRecord):
    """Custom LogRecord with additional attributes for WebLens"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.browser: Optional[str] = None
        self.profile: Optional[str] = None

# Global console instance
console = Console()


class WebLensFormatter(logging.Formatter):
    """Custom formatter for WebLens logs"""
    
    def __init__(self):
        super().__init__(
            fmt="%(asctime)s | %(name)s | %(levelname)s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
    
    def format(self, record: logging.LogRecord) -> str:
        # Add extra context if available
        if hasattr(record, 'browser') and getattr(record, 'browser'):
            record.name = f"{record.name}[{getattr(record, 'browser')}]"
        if hasattr(record, 'profile') and getattr(record, 'profile'):
            record.name = f"{record.name}[{getattr(record, 'profile')}]"
        
        return super().format(record)


def setup_logging(level: str = "INFO", log_file: Optional[str] = None) -> Path:
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
        log_file_path = config.logs_dir / f"weblens_{timestamp}.log"
    else:
        log_file_path = Path(log_file)
    
    file_handler = logging.FileHandler(str(log_file_path), encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)  # Always log everything to file
    
    # Custom formatter for file
    file_formatter = WebLensFormatter()
    file_handler.setFormatter(file_formatter)
    
    root_logger.addHandler(file_handler)
    
    # Silence some noisy loggers
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    logging.getLogger("asyncio").setLevel(logging.WARNING)
    
    return log_file_path


def get_logger(name: str) -> logging.Logger:
    """Get a logger instance for a module"""
    return logging.getLogger(name)


class BrowserContextLogger:
    """Context manager for adding browser/profile context to logs"""
    
    def __init__(self, logger: logging.Logger, browser: str, profile: Optional[str] = None):
        self.logger = logger
        self.browser = browser
        self.profile = profile
        self.old_factory: Optional[Any] = None
    
    def __enter__(self) -> logging.Logger:
        self.old_factory = logging.getLogRecordFactory()
        
        def record_factory(*args, **kwargs) -> logging.LogRecord:
            record = self.old_factory(*args, **kwargs) if self.old_factory else logging.LogRecord(*args, **kwargs)
            # Use setattr to avoid type checker issues with dynamic attributes
            setattr(record, 'browser', self.browser)
            if self.profile:
                setattr(record, 'profile', self.profile)
            return record
        
        logging.setLogRecordFactory(record_factory)
        return self.logger
    
    def __exit__(self, exc_type: Optional[type], exc_val: Optional[Exception], exc_tb: Optional[Any]) -> None:
        if self.old_factory:
            logging.setLogRecordFactory(self.old_factory)
