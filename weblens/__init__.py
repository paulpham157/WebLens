"""
WebLens - Advanced Web Testing Framework
=========================================

WebLens is a modern web testing framework that leverages browser-use
for intelligent browser automation with multi-profile support.

Key Features:
- Multi-profile browser management
- Intelligent web automation using browser-use
- Support for Chrome, Firefox, Safari, and Edge
- Parallel test execution
- Rich reporting and logging
- Easy configuration management
"""

__version__ = "0.1.0"
__author__ = "Paul Pham 157"
__email__ = "paulpham157@gmail.com"

from .config import Config
from .core import BrowserManager
from .profiles import ProfileManager
from .utils import get_logger

__all__ = ["Config", "BrowserManager", "ProfileManager", "get_logger"]
