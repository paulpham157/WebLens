"""
Legacy Functions for Browser Use API

This module provides legacy function wrappers for backward compatibility.
"""
from typing import Dict, Any

from .api.client import BrowserUseClient
from .controllers.task_controller import TaskController
from .controllers.media_manager import MediaManager
from .controllers.task_monitor import TaskMonitor

def create_task(instructions: str, **kwargs) -> str:
    """Legacy function that redirects to BrowserUseClient.create_task"""
    print("ℹ️ This function is deprecated. Use BrowserUseClient.create_task() instead.")
    client = BrowserUseClient()
    return client.create_task(instructions, **kwargs)

def create_structured_task(instructions: str, schema: dict, **kwargs) -> str:
    """Legacy function that redirects to BrowserUseClient.create_structured_task"""
    print("ℹ️ This function is deprecated. Use BrowserUseClient.create_structured_task() instead.")
    client = BrowserUseClient()
    return client.create_structured_task(instructions, schema, **kwargs)

def get_task_status(task_id: str) -> str:
    """Legacy function that redirects to BrowserUseClient.get_task_status"""
    print("ℹ️ This function is deprecated. Use BrowserUseClient.get_task_status() instead.")
    client = BrowserUseClient()
    return client.get_task_status(task_id)

def get_task_details(task_id: str) -> Dict[str, Any]:
    """Legacy function that redirects to BrowserUseClient.get_task_details"""
    print("ℹ️ This function is deprecated. Use BrowserUseClient.get_task_details() instead.")
    client = BrowserUseClient()
    return client.get_task_details(task_id)

def fetch_task_output(task_id: str) -> Any:
    """Legacy function that redirects to BrowserUseClient.fetch_task_output"""
    print("ℹ️ This function is deprecated. Use BrowserUseClient.fetch_task_output() instead.")
    client = BrowserUseClient()
    return client.fetch_task_output(task_id)

def wait_for_task_completion(task_id: str, poll_interval: int = 5):
    """Legacy function that redirects to BrowserUseClient.wait_for_task_completion"""
    print("ℹ️ This function is deprecated. Use BrowserUseClient.wait_for_task_completion() instead.")
    client = BrowserUseClient()
    client.wait_for_task_completion(task_id, poll_interval)

def monitor_task_progress(task_id: str, show_steps: bool = True):
    """Legacy function that redirects to TaskMonitor.monitor_task_progress"""
    print("ℹ️ This function is deprecated. Use TaskMonitor.monitor_task_progress() instead.")
    monitor = TaskMonitor()
    return monitor.monitor_task_progress(task_id, show_steps)

def stop_task(task_id: str):
    """Legacy function that redirects to TaskController.stop_task"""
    print("ℹ️ This function is deprecated. Use TaskController.stop_task() instead.")
    controller = TaskController()
    return controller.stop_task(task_id)

def pause_task(task_id: str):
    """Legacy function that redirects to TaskController.pause_task"""
    print("ℹ️ This function is deprecated. Use TaskController.pause_task() instead.")
    controller = TaskController()
    return controller.pause_task(task_id)

def resume_task(task_id: str):
    """Legacy function that redirects to TaskController.resume_task"""
    print("ℹ️ This function is deprecated. Use TaskController.resume_task() instead.")
    controller = TaskController()
    return controller.resume_task(task_id)

def get_task_media(task_id: str):
    """Legacy function that redirects to MediaManager.get_task_media"""
    print("ℹ️ This function is deprecated. Use MediaManager.get_task_media() instead.")
    media_manager = MediaManager()
    return media_manager.get_task_media(task_id)

def get_task_screenshots(task_id: str):
    """Legacy function that redirects to MediaManager.get_task_screenshots"""
    print("ℹ️ This function is deprecated. Use MediaManager.get_task_screenshots() instead.")
    media_manager = MediaManager()
    return media_manager.get_task_screenshots(task_id)

def get_task_gif(task_id: str):
    """Legacy function that redirects to MediaManager.get_task_gif"""
    print("ℹ️ This function is deprecated. Use MediaManager.get_task_gif() instead.")
    media_manager = MediaManager()
    return media_manager.get_task_gif(task_id)

def get_presigned_upload_url(filename: str):
    """Legacy function that redirects to MediaManager.get_presigned_upload_url"""
    print("ℹ️ This function is deprecated. Use MediaManager.get_presigned_upload_url() instead.")
    media_manager = MediaManager()
    return media_manager.get_presigned_upload_url(filename)

def upload_file_to_presigned_url(presigned_url: str, file_path: str):
    """Legacy function that redirects to MediaManager.upload_file_to_presigned_url"""
    print("ℹ️ This function is deprecated. Use MediaManager.upload_file_to_presigned_url() instead.")
    return MediaManager.upload_file_to_presigned_url(presigned_url, file_path)
