"""
WebLens Configuration
"""
import os
from pathlib import Path
from typing import Dict, Any

# Load environment variables from .env file
try:
    from dotenv import load_dotenv
    # Load from project root
    env_path = Path(__file__).parent.parent / ".env"
    load_dotenv(env_path)
except ImportError:
    # dotenv not available, use os.environ only
    pass


class Config:
    """WebLens configuration class for browser-use cloud"""
    
    def __init__(self):
        # Base paths
        self.project_root = Path(__file__).parent.parent
        self.logs_dir = self.project_root / "logs"
        self.screenshots_dir = self.project_root / "screenshots"
        self.videos_dir = self.project_root / "videos"
        self.reports_dir = self.project_root / "reports"
        self.browser_profiles_dir = self.project_root / "browser_profiles"
        
        # Ensure directories exist
        for directory in [self.logs_dir, self.screenshots_dir, self.videos_dir, 
                         self.reports_dir, self.browser_profiles_dir]:
            directory.mkdir(exist_ok=True)
        
        # Browser-use Cloud API settings
        self.browser_use_api_key = os.getenv("BROWSER_USE_API_KEY", "")
        self.browser_use_base_url = os.getenv("BROWSER_USE_BASE_URL", "https://api.browser-use.com/api/v1")
        
        # Test settings
        self.test_base_url = os.getenv("TEST_BASE_URL", "https://practicetestautomation.com/practice-test-login/")
        self.test_parallel_workers = int(os.getenv("TEST_PARALLEL_WORKERS", "3"))
        self.test_timeout = int(os.getenv("TEST_TIMEOUT", "30000"))
        
        # Logging settings
        self.log_level = os.getenv("LOG_LEVEL", "INFO")
        self.log_file = os.getenv("LOG_FILE", "logs/weblens.log")
    
    def get_browser_use_config(self) -> Dict[str, Any]:
        """Get browser-use cloud configuration"""
        if not self.browser_use_api_key:
            raise ValueError("BROWSER_USE_API_KEY environment variable is required")
        
        return {
            "api_key": self.browser_use_api_key,
            "base_url": self.browser_use_base_url,
            "timeout": self.test_timeout,
            "max_workers": self.test_parallel_workers
        }
    
    def validate_config(self) -> bool:
        """Validate configuration"""
        if not self.browser_use_api_key:
            return False
        if not self.browser_use_base_url:
            return False
        return True


# Global config instance
config = Config()