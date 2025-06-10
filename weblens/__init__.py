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
__author__ = "Paul Pham"
__email__ = "paulpham157@example.com"

from .core.browser_manager import BrowserManager
from .core.test_runner import TestRunner
from .profiles.profile_manager import ProfileManager

__all__ = ["BrowserManager", "TestRunner", "ProfileManager"]
