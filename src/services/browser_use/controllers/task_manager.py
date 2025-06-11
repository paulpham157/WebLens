"""
Task Manager for Browser Use API

This module provides enhanced task management functionality for Browser Use API.
"""
import time
from typing import Dict, Any, Optional

from ..constants import BASE_URL, API_KEY
from ..api.client import BrowserUseClient
from ..controllers.task_monitor import TaskMonitor
from ..controllers.task_controller import TaskController
from ..models.models import SocialMediaCompanies

class TaskManager:
    """Enhanced task management class"""
    
    def __init__(self, base_url: Optional[str] = None, api_key: Optional[str] = None):
        self.base_url = base_url or BASE_URL
        self.api_key = api_key or API_KEY
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        self.active_tasks = {}
        self.completed_tasks = {}
        self.client = BrowserUseClient(self.base_url, self.api_key)
        self.monitor = TaskMonitor(self.base_url, self.api_key)
        self.controller = TaskController(self.base_url, self.api_key)
    
    def create_and_track_task(self, instructions: str, task_name: Optional[str] = None, **kwargs) -> str:
        """Create a task and add it to tracking"""
        task_id = self.client.create_task(instructions, **kwargs)
        
        task_info = {
            'id': task_id,
            'name': task_name or f"Task_{task_id[:8]}",
            'instructions': instructions,
            'created_at': time.time(),
            'kwargs': kwargs
        }
        
        self.active_tasks[task_id] = task_info
        print(f"✅ Created and tracking task: {task_info['name']} ({task_id})")
        return task_id
    
    def monitor_all_tasks(self):
        """Monitor all active tasks"""
        if not self.active_tasks:
            print("No active tasks to monitor")
            return
        
        print(f"📊 Monitoring {len(self.active_tasks)} active tasks...")
        
        for task_id, task_info in list(self.active_tasks.items()):
            try:
                status = self.client.get_task_status(task_id)
                print(f"🔄 {task_info['name']}: {status}")
                
                if status in ['finished', 'failed', 'stopped']:
                    # Move to completed tasks
                    task_info['completed_at'] = time.time()
                    task_info['final_status'] = status
                    
                    if status == 'finished':
                        details = self.client.get_task_details(task_id)
                        task_info['output'] = details.get('output')
                    
                    self.completed_tasks[task_id] = task_info
                    del self.active_tasks[task_id]
                    print(f"✅ {task_info['name']} completed with status: {status}")
            
            except Exception as e:
                print(f"❌ Error checking {task_info['name']}: {e}")
    
    def get_task_summary(self):
        """Get summary of all tasks"""
        return {
            'active_count': len(self.active_tasks),
            'completed_count': len(self.completed_tasks),
            'active_tasks': list(self.active_tasks.keys()),
            'completed_tasks': list(self.completed_tasks.keys())
        }
    
    def stop_all_active_tasks(self):
        """Stop all active tasks"""
        for task_id, task_info in self.active_tasks.items():
            try:
                self.controller.stop_task(task_id)
                print(f"🛑 Stopped {task_info['name']}")
            except Exception as e:
                print(f"❌ Failed to stop {task_info['name']}: {e}")
    
    def structured_output_example(self):
        """Example function demonstrating structured output usage"""
        schema = SocialMediaCompanies.model_json_schema()
        task_id = self.client.create_structured_task(
            "Get me the top social media companies by market cap",
            schema
        )
        print(f"Task created with ID: {task_id}")

        self.client.wait_for_task_completion(task_id)
        print("Task completed!")

        output = self.client.fetch_task_output(task_id)
        print("Raw output:", output)

        try:
            parsed = SocialMediaCompanies.model_validate_json(output)
            print("Parsed output:")
            print(parsed)
        except Exception as e:
            print(f"Failed to parse structured output: {e}")
