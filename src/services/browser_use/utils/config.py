"""
Configuration Management for Browser Use API

This module provides configuration management functionality for Browser Use API.
"""
import os
import json
from typing import Dict, Any

from ..constants import BASE_URL, API_KEY

class ConfigManager:
    """Configuration management for Browser Use API"""
    
    def __init__(self):
        self.default_config = {
            'llm_model': 'gpt-4o',
            'use_adblock': True,
            'use_proxy': True,
            'proxy_country_code': 'us',
            'highlight_elements': False,
            'save_browser_data': False
        }
    
    def get_config_for_task_type(self, task_type: str) -> Dict[str, Any]:
        """Get optimized configuration for different task types"""
        configs = {
            'web_scraping': {
                **self.default_config,
                'use_adblock': True,
                'highlight_elements': False,
                'save_browser_data': False
            },
            'form_filling': {
                **self.default_config,
                'highlight_elements': True,
                'save_browser_data': True,
                'use_proxy': False
            },
            'social_media': {
                **self.default_config,
                'save_browser_data': True,
                'proxy_country_code': 'us'
            },
            'ecommerce': {
                **self.default_config,
                'save_browser_data': True,
                'highlight_elements': True
            }
        }
        
        return configs.get(task_type, self.default_config)
    
    def setup_environment(self):
        """Setup and validate environment for Browser Use API"""
        print("🔧 Setting up Browser Use API environment...")
        
        # Check for .env file
        env_file = ".env"
        if not os.path.exists(env_file):
            print("⚠️ No .env file found. Creating example...")
            self.create_env_example()
        
        # Check environment variables
        required_vars = ["BROWSER_USE_API_KEY"]
        optional_vars = ["BROWSER_USE_BASE_URL"]
        
        print("\n📋 Environment Variables:")
        for var in required_vars:
            value = os.getenv(var)
            if value and value != "your_api_key_here":
                print(f"  ✅ {var}: Configured")
            else:
                print(f"  ❌ {var}: Not configured")
        
        for var in optional_vars:
            value = os.getenv(var)
            if value:
                print(f"  ✅ {var}: {value}")
            else:
                print(f"  ℹ️ {var}: Using default")
    
    @staticmethod
    def create_env_example():
        """Create an example .env file"""
        env_content = """# Browser Use API Configuration
BROWSER_USE_API_KEY=your_browser_use_api_key_here
BROWSER_USE_BASE_URL=https://api.browser-use.com/api/v1

# Optional: Test settings
TEST_PARALLEL_WORKERS=3
TEST_TIMEOUT=30000

# Optional: Logging
LOG_LEVEL=INFO
LOG_FILE=logs/weblens.log
"""
        
        with open(".env.example", "w") as f:
            f.write(env_content)
        
        print("📄 Created .env.example file")
        print("💡 Copy it to .env and add your API key")
    
    @staticmethod
    def get_api_info() -> Dict[str, Any]:
        """Get API configuration information"""
        info = {
            "base_url": BASE_URL,
            "api_key_configured": API_KEY != "your_api_key_here" and bool(API_KEY),
            "api_key_preview": f"{API_KEY[:10]}..." if API_KEY and API_KEY != "your_api_key_here" else "Not configured"
        }
        
        print("📊 API Configuration:")
        print(f"  Base URL: {info['base_url']}")
        print(f"  API Key: {'✅ Configured' if info['api_key_configured'] else '❌ Not configured'}")
        if info['api_key_configured']:
            print(f"  Key Preview: {info['api_key_preview']}")
        
        return info
