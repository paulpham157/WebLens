"""
Help and Documentation for Browser Use API

This module provides help and documentation functions for Browser Use API.
"""

def print_refactored_api_help():
    """Print information about the refactored class-based API structure"""
    help_text = """
🔧 Browser Use API - Refactored Class-Based Structure
=====================================================

This module has been refactored into a class-based structure for better organization,
maintainability, and code reuse. The main classes are:

CORE CLASSES:
- BrowserUseClient - Core API client for basic task operations
- TaskController - Handle task control operations (pause, resume, stop)
- MediaManager - Handle media and file operations
- TaskMonitor - Monitor task progress with real-time feedback

ADVANCED FEATURES:
- TaskManager - Enhanced task management with tracking
- BatchTaskManager - Manage multiple tasks in batch
- ConfigManager - Handle configuration options
- ValidationUtils - API validation and error handling
- SpecializedTaskCreator - Create tasks for specific use cases
- QuickActions - Convenience functions for common tasks

MODELS:
- SocialMediaCompanies, WebsiteAnalysis, etc. - Pydantic models for structured output

EXAMPLES:
- BrowserUseExamples - Example functions demonstrating API capabilities

USAGE EXAMPLES:

# Basic client usage
client = BrowserUseClient()
task_id = client.create_task("Go to google.com and search for 'AI news'")
result = client.get_task_details(task_id)

# Task control
controller = TaskController()
controller.pause_task(task_id)
controller.resume_task(task_id)

# Media operations
media = MediaManager()
screenshots = media.get_task_screenshots(task_id)

# Task monitoring
monitor = TaskMonitor()
monitor.monitor_task_progress(task_id)

# Quick operations
quick = QuickActions()
results = quick.quick_web_scrape("https://example.com")

Legacy functions are still available for backward compatibility,
but will print deprecation notices encouraging use of the class-based API.
"""
    print(help_text)


def print_api_help():
    """Print help information about the Browser Use API"""
    help_text = """
🚀 Browser Use API Helper
========================

This module provides a comprehensive interface to the Browser Use API.
Browser Use allows you to automate browser tasks using natural language.

BASIC OPERATIONS:
- create_task() - Create a browser task
- get_task_status() - Check task status 
- get_task_details() - Get full task details
- fetch_task_output() - Get task output

TASK CONTROL:
- pause_task() - Pause running task
- resume_task() - Resume paused task  
- stop_task() - Stop task permanently

MEDIA & FILES:
- get_task_media() - Get task recordings
- get_task_screenshots() - Get task screenshots
- get_task_gif() - Get task GIF
- get_presigned_upload_url() - Get file upload URL
- upload_file_to_presigned_url() - Upload files

ADVANCED FEATURES:
- TaskManager class - Track and manage multiple tasks
- Batch operations - Create and manage multiple tasks
- ConfigManager - Optimize settings for different task types
- SpecializedTaskCreator - Create tasks for common use cases

QUICK START FUNCTIONS:
- quick_web_scrape() - Simple web scraping
- quick_form_fill() - Form filling automation
- quick_price_check() - Price comparison

UTILITY FUNCTIONS:
- validate_api_connection() - Test API connectivity
- monitor_task_progress() - Enhanced progress monitoring
- export_task_results() - Export results to JSON
- print_api_usage_examples() - Show usage examples

CONFIGURATION:
Set these environment variables:
- BROWSER_USE_API_KEY: Your API key
- BROWSER_USE_BASE_URL: API base URL (optional)

For detailed examples, run:
from browser_use import BrowserUseExamples
examples = BrowserUseExamples()
examples.run_all_demos()

For information about the refactored class-based API structure, run:
from browser_use import print_refactored_api_help
print_refactored_api_help()
"""
    print(help_text)
