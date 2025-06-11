"""
Task Control Operations for Browser Use API

This module provides task control operations for Browser Use API.
"""
import requests
from typing import Dict, Any, Optional

from ..constants import BASE_URL, API_KEY

class TaskController:
    """Handle task control operations like pause, resume, stop"""
    
    def __init__(self, base_url: Optional[str] = None, api_key: Optional[str] = None):
        self.base_url = base_url or BASE_URL
        self.api_key = api_key or API_KEY
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    def stop_task(self, task_id: str) -> Dict[str, Any]:
        """Stop a running browser automation task immediately"""
        response = requests.put(f"{self.base_url}/stop-task", headers=self.headers, params={'task_id': task_id})
        response.raise_for_status()
        return response.json()
    
    def pause_task(self, task_id: str) -> Dict[str, Any]:
        """Pause execution of a running task"""
        response = requests.put(f"{self.base_url}/pause-task", headers=self.headers, params={'task_id': task_id})
        response.raise_for_status()
        return response.json()
    
    def resume_task(self, task_id: str) -> Dict[str, Any]:
        """Resume execution of a previously paused task"""
        response = requests.put(f"{self.base_url}/resume-task", headers=self.headers, params={'task_id': task_id})
        response.raise_for_status()
        return response.json()
