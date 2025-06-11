"""
Core API Client for Browser Use API

This module provides the core client for interacting with the Browser Use API.
"""
import requests
import json
import time
from typing import Dict, Any, Optional

from ..constants import BASE_URL, API_KEY

class BrowserUseClient:
    """Core Browser Use API client for basic task operations"""
    
    def __init__(self, base_url: Optional[str] = None, api_key: Optional[str] = None):
        self.base_url = base_url or BASE_URL
        self.api_key = api_key or API_KEY
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    def create_task(self, instructions: str, **kwargs) -> str:
        """
        Create a new browser automation task with full parameter support

        Args:
            instructions (str): What should the agent do
            **kwargs: Additional parameters:
                - secrets (dict): Dictionary of secrets to be used by the agent
                - allowed_domains (list): List of domains that the agent is allowed to visit
                - save_browser_data (bool): If True, browser cookies will be saved
                - structured_output_json (str): JSON schema for structured output
                - llm_model (str): LLM model to use (default: gpt-4o)
                - use_adblock (bool): If True, agent will use an adblocker
                - use_proxy (bool): If True, agent will use a proxy
                - proxy_country_code (str): Country code for proxy ('us', 'fr', 'it', 'jp', 'au', 'de', 'fi', 'ca')
                - highlight_elements (bool): If True, agent will highlight elements
                - included_file_names (list): File names to include in the task

        Returns:
            str: Task ID
        """
        payload = {'task': instructions}
        
        # Add optional parameters if provided
        optional_params = [
            'secrets', 'allowed_domains', 'save_browser_data', 
            'structured_output_json', 'llm_model', 'use_adblock', 
            'use_proxy', 'proxy_country_code', 'highlight_elements', 
            'included_file_names'
        ]
        
        for param in optional_params:
            if param in kwargs:
                payload[param] = kwargs[param]
        
        response = requests.post(f"{self.base_url}/run-task", headers=self.headers, json=payload)
        if response.status_code == 200:
            return response.json()['id']
        else:
            raise Exception(f"Error: {response.status_code} - {response.text}")
    
    def create_structured_task(self, instructions: str, schema: dict, **kwargs) -> str:
        """Create a task that expects structured output with full parameter support"""
        payload = {
            "task": instructions,
            "structured_output_json": json.dumps(schema)
        }
        
        # Add optional parameters if provided
        optional_params = [
            'secrets', 'allowed_domains', 'save_browser_data', 
            'llm_model', 'use_adblock', 'use_proxy', 'proxy_country_code', 
            'highlight_elements', 'included_file_names'
        ]
        
        for param in optional_params:
            if param in kwargs:
                payload[param] = kwargs[param]
        
        response = requests.post(f"{self.base_url}/run-task", headers=self.headers, json=payload)
        response.raise_for_status()
        return response.json()["id"]
    
    def get_task_status(self, task_id: str) -> str:
        """Get current task status"""
        response = requests.get(f'{self.base_url}/task/{task_id}/status', headers=self.headers)
        return response.json()
    
    def get_task_details(self, task_id: str) -> Dict[str, Any]:
        """Get full task details including output"""
        response = requests.get(f'{self.base_url}/task/{task_id}', headers=self.headers)
        return response.json()
    
    def fetch_task_output(self, task_id: str) -> Any:
        """Retrieve the final task result"""
        response = requests.get(f"{self.base_url}/task/{task_id}", headers=self.headers)
        response.raise_for_status()
        return response.json()["output"]
    
    def wait_for_task_completion(self, task_id: str, poll_interval: int = 5):
        """Poll task status until it completes"""
        while True:
            response = requests.get(f"{self.base_url}/task/{task_id}/status", headers=self.headers)
            response.raise_for_status()
            status = response.json()
            if status == "finished":
                break
            elif status in ["failed", "stopped"]:
                raise RuntimeError(f"Task {task_id} ended with status: {status}")
            print("Waiting for task to finish...")
            time.sleep(poll_interval)
    
    def get_task_full_info(self, task_id: str) -> Dict[str, Any]:
        """Get comprehensive task information including all available data"""
        try:
            details = self.get_task_details(task_id)
            info = {
                'task_details': details,
                'status': self.get_task_status(task_id)
            }
            
            # Add media if task is completed
            if details.get('status') in ['finished', 'failed', 'stopped']:
                try:
                    # Avoid circular imports by importing MediaManager only when needed
                    from ..controllers.media_manager import MediaManager
                    media_manager = MediaManager(self.base_url, self.api_key)
                    info['media'] = media_manager.get_task_media(task_id)
                    info['screenshots'] = media_manager.get_task_screenshots(task_id)
                except Exception as media_error:
                    # Log the error or add to info dictionary
                    info['media_error'] = str(media_error)
            
            return info
        except Exception as e:
            raise Exception(f"Failed to get task info: {e}")
