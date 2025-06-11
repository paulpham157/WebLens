"""
Account Management for Browser Use API

This module provides account management functionality for Browser Use API.
"""
import requests
from typing import Dict, Any, Optional

from ..constants import BASE_URL, API_KEY

class AccountManager:
    """Handle account management operations like checking balance"""
    
    def __init__(self, base_url: Optional[str] = None, api_key: Optional[str] = None):
        self.base_url = base_url or BASE_URL
        self.api_key = api_key or API_KEY
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    def get_account_balance(self) -> Dict[str, Any]:
        """
        Get current account balance and usage information
        
        Returns:
            Dictionary containing balance information like:
            {
                "credits_remaining": 100.0,
                "credits_used": 50.0,
                "total_credits": 150.0,
                "usage_details": {
                    "tasks_completed": 25,
                    "tasks_failed": 3
                }
            }
        """
        response = requests.get(f"{self.base_url}/account/balance", headers=self.headers)
        response.raise_for_status()
        return response.json()
    
    def get_account_info(self) -> Dict[str, Any]:
        """
        Get detailed account information
        
        Returns:
            Dictionary containing account information including subscription plan, limits, etc.
        """
        response = requests.get(f"{self.base_url}/account/info", headers=self.headers)
        response.raise_for_status()
        return response.json()
    
    def get_usage_history(self, days: int = 30) -> Dict[str, Any]:
        """
        Get account usage history
        
        Args:
            days: Number of days of history to retrieve (default: 30)
            
        Returns:
            Dictionary containing usage history
        """
        response = requests.get(
            f"{self.base_url}/account/usage", 
            headers=self.headers,
            params={"days": days}
        )
        response.raise_for_status()
        return response.json()
