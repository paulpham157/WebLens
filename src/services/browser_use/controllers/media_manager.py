"""
Media and File Management for Browser Use API

This module provides media and file management functionality for Browser Use API.
"""
import requests
from typing import Dict, Any, Optional

from ..constants import BASE_URL, API_KEY

class MediaManager:
    """Handle media and file operations"""
    
    def __init__(self, base_url: Optional[str] = None, api_key: Optional[str] = None):
        self.base_url = base_url or BASE_URL
        self.api_key = api_key or API_KEY
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    def get_task_media(self, task_id: str) -> Dict[str, Any]:
        """Returns links to any recordings or media generated during task execution"""
        response = requests.get(f'{self.base_url}/task/{task_id}/media', headers=self.headers)
        return response.json()
    
    def get_task_screenshots(self, task_id: str) -> Dict[str, Any]:
        """Returns screenshot URLs generated during task execution"""
        response = requests.get(f"{self.base_url}/task/{task_id}/screenshots", headers=self.headers)
        response.raise_for_status()
        return response.json()
    
    def get_task_gif(self, task_id: str) -> Dict[str, Any]:
        """Returns GIF URL of the task execution"""
        response = requests.get(f"{self.base_url}/task/{task_id}/gif", headers=self.headers)
        response.raise_for_status()
        return response.json()
    
    def get_presigned_upload_url(self, filename: str) -> Dict[str, Any]:
        """Get presigned URL for uploading files"""
        response = requests.post(f"{self.base_url}/uploads/presigned-url", headers=self.headers, json={'filename': filename})
        response.raise_for_status()
        return response.json()
    
    @staticmethod
    def upload_file_to_presigned_url(presigned_url: str, file_path: str) -> bool:
        """Upload a file to the presigned URL"""
        with open(file_path, 'rb') as file:
            response = requests.put(presigned_url, data=file)
            response.raise_for_status()
        return response.status_code == 200
