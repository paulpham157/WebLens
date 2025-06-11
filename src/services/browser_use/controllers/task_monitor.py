"""
Task Monitor and Progress Tracking for Browser Use API

This module provides task monitoring functionality for Browser Use API.
"""
import json
import time
from typing import Dict, Any, Optional

from ..constants import BASE_URL, API_KEY
from ..api.client import BrowserUseClient

class TaskMonitor:
    """Monitor task progress with real-time feedback"""
    
    def __init__(self, base_url: Optional[str] = None, api_key: Optional[str] = None):
        self.base_url = base_url or BASE_URL
        self.api_key = api_key or API_KEY
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        self.client = BrowserUseClient(self.base_url, self.api_key)
    
    def wait_for_completion(self, task_id: str, poll_interval: int = 2, show_steps: bool = True):
        """
        Poll task status until completion with step tracking
        
        Args:
            task_id: The task ID to monitor
            poll_interval: How often to check for updates (in seconds)
            show_steps: Whether to print step details
            
        Returns:
            The complete task details once finished
        """
        count = 0
        unique_steps = []
        
        while True:
            details = self.client.get_task_details(task_id)
            status = details['status']
            
            # Track and display new steps
            if show_steps:
                new_steps = details.get('steps', [])
                if new_steps != unique_steps:
                    for step in new_steps:
                        if step not in unique_steps:
                            print(json.dumps(step, indent=4))
                    unique_steps = new_steps
            
            count += 1
            
            # Check if task is complete
            if status in ['finished', 'failed', 'stopped']:
                return details
                
            time.sleep(poll_interval)
    
    def monitor_task_progress(self, task_id: str, show_steps: bool = True):
        """
        Monitor task progress with enhanced output
        
        Args:
            task_id: The task ID to monitor
            show_steps: Whether to show detailed steps
            
        Returns:
            The complete task details once finished
        """
        print(f"📊 Monitoring task: {task_id}")
        
        count = 0
        unique_steps = []
        
        while True:
            try:
                details = self.client.get_task_details(task_id)
                status = details['status']
                print(f"Status: {status} | Steps completed: {len(details.get('steps', []))}")
                
                if show_steps:
                    new_steps = details.get('steps', [])
                    if new_steps != unique_steps:
                        for step in new_steps:
                            if step not in unique_steps:
                                print(f"📝 Step {step.get('step', '?')}: {step.get('next_goal', 'Processing...')}")
                        unique_steps = new_steps
                
                if status in ['finished', 'failed', 'stopped']:
                    print(f"🏁 Task {status}!")
                    if status == 'finished':
                        print(f"📤 Output: {details.get('output', 'No output')}")
                    return details
                    
                count += 1
                time.sleep(2)
                
            except Exception as e:
                print(f"❌ Error monitoring task: {e}")
                break
        
        return None
