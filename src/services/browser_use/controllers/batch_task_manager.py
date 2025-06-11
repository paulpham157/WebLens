"""
Batch Task Management for Browser Use API

This module provides batch task management functionality for Browser Use API.
"""
import time
from datetime import datetime
from typing import Dict, Any, Optional, List

from ..constants import BASE_URL, API_KEY
from ..api.client import BrowserUseClient

class BatchTaskManager:
    """Manage multiple tasks in batch"""
    
    def __init__(self, base_url: Optional[str] = None, api_key: Optional[str] = None):
        self.base_url = base_url or BASE_URL
        self.api_key = api_key or API_KEY
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        self.client = BrowserUseClient(self.base_url, self.api_key)
    
    def create_batch_tasks(self, task_configs: List[dict]) -> List[str]:
        """
        Create multiple tasks in batch
        
        Args:
            task_configs: List of task configuration dictionaries, each containing:
                - instructions: The task instructions (required)
                - Additional optional parameters
                
        Returns:
            List of created task IDs
        """
        task_ids = []
        
        for i, config in enumerate(task_configs, 1):
            try:
                instructions = config.pop('instructions')
                task_id = self.client.create_task(instructions, **config)
                task_ids.append(task_id)
                print(f"✅ Created batch task {i}/{len(task_configs)}: {task_id}")
            except Exception as e:
                print(f"❌ Failed to create batch task {i}: {e}")
        
        return task_ids
    
    def wait_for_batch_completion(self, task_ids: List[str], poll_interval: int = 5) -> Dict[str, Any]:
        """
        Wait for multiple tasks to complete
        
        Args:
            task_ids: List of task IDs to monitor
            poll_interval: How often to check statuses (in seconds)
            
        Returns:
            Dictionary of task IDs to completion results
        """
        print(f"⏳ Waiting for {len(task_ids)} tasks to complete...")
        
        completed_tasks = {}
        remaining_tasks = set(task_ids)
        
        while remaining_tasks:
            for task_id in list(remaining_tasks):
                try:
                    status = self.client.get_task_status(task_id)
                    
                    if status in ['finished', 'failed', 'stopped']:
                        details = self.client.get_task_details(task_id)
                        completed_tasks[task_id] = {
                            'status': status,
                            'output': details.get('output') if status == 'finished' else None
                        }
                        remaining_tasks.remove(task_id)
                        print(f"✅ Task {task_id} completed: {status}")
                
                except Exception as e:
                    print(f"❌ Error checking task {task_id}: {e}")
                    remaining_tasks.remove(task_id)
            
            if remaining_tasks:
                print(f"⏳ {len(remaining_tasks)} tasks still running...")
                time.sleep(poll_interval)
        
        print("🎉 All batch tasks completed!")
        return completed_tasks
    
    def get_task_statistics(self, task_ids: List[str]) -> Dict[str, Any]:
        """
        Get statistics for a list of tasks
        
        Args:
            task_ids: List of task IDs to analyze
            
        Returns:
            Dictionary of statistics
        """
        stats = {
            'total_tasks': len(task_ids),
            'finished': 0,
            'failed': 0,
            'running': 0,
            'stopped': 0,
            'average_duration': 0.0,
            'total_steps': 0
        }
        
        durations = []
        
        for task_id in task_ids:
            try:
                details = self.client.get_task_details(task_id)
                status = details.get('status', 'unknown')
                
                if status == 'finished':
                    stats['finished'] += 1
                elif status == 'failed':
                    stats['failed'] += 1
                elif status in ['running', 'created']:
                    stats['running'] += 1
                elif status == 'stopped':
                    stats['stopped'] += 1
                
                # Calculate duration if completed
                if details.get('created_at') and details.get('finished_at'):
                    try:
                        created = datetime.fromisoformat(details['created_at'].replace('Z', '+00:00'))
                        finished = datetime.fromisoformat(details['finished_at'].replace('Z', '+00:00'))
                        duration = (finished - created).total_seconds()
                        durations.append(duration)
                    except:
                        pass
                
                # Count steps
                steps = details.get('steps', [])
                stats['total_steps'] += len(steps)
                
            except Exception as e:
                print(f"⚠️ Could not get stats for task {task_id}: {e}")
        
        if durations:
            stats['average_duration'] = sum(durations) / len(durations)
        
        return stats
    
    def print_task_statistics(self, task_ids: List[str]):
        """Print formatted task statistics"""
        stats = self.get_task_statistics(task_ids)
        
        print("📊 Task Statistics:")
        print(f"  Total Tasks: {stats['total_tasks']}")
        print(f"  ✅ Finished: {stats['finished']}")
        print(f"  ❌ Failed: {stats['failed']}")
        print(f"  🔄 Running: {stats['running']}")
        print(f"  🛑 Stopped: {stats['stopped']}")
        print(f"  📝 Total Steps: {stats['total_steps']}")
        
        if stats['average_duration'] > 0:
            print(f"  ⏱️ Average Duration: {stats['average_duration']:.1f} seconds")
