"""
Examples and Demo Helpers for Browser Use API

This module provides example functions demonstrating Browser Use API capabilities.
"""
import time
from typing import Dict, Any, Optional

from ..constants import BASE_URL, API_KEY
from ..api.client import BrowserUseClient
from ..controllers.task_controller import TaskController
from ..controllers.task_monitor import TaskMonitor
from ..controllers.media_manager import MediaManager
from ..controllers.task_manager import TaskManager
from ..controllers.batch_task_manager import BatchTaskManager
from ..controllers.specialized_task_creator import SpecializedTaskCreator
from ..utils.validation import ValidationUtils
from ..models.models import SocialMediaCompanies

class BrowserUseExamples:
    """Example functions demonstrating Browser Use API capabilities"""
    
    def __init__(self, base_url: Optional[str] = None, api_key: Optional[str] = None):
        self.base_url = base_url or BASE_URL
        self.api_key = api_key or API_KEY
        self.client = BrowserUseClient(self.base_url, self.api_key)
        self.controller = TaskController(self.base_url, self.api_key)
        self.monitor = TaskMonitor(self.base_url, self.api_key)
        self.media_manager = MediaManager(self.base_url, self.api_key)
        
    def control_task_example(self):
        """Example of task control with pause/resume functionality"""
        # Create a new task
        task_id = self.client.create_task("Go to google.com and search for Browser Use")

        # Wait for 5 seconds
        time.sleep(5)

        # Pause the task
        self.controller.pause_task(task_id)
        print("Task paused! Check the live preview.")

        # Wait for user input
        input("Press Enter to resume...")

        # Resume the task
        self.controller.resume_task(task_id)

        # Wait for completion
        result = self.monitor.wait_for_completion(task_id)
        print(f"Task completed with output: {result['output']}")

    def advanced_task_example(self):
        """Example demonstrating advanced task creation with all parameters"""
        task_id = self.client.create_task(
            "Search for the latest AI news and summarize the top 3 articles",
            secrets={"api_key": "your_news_api_key"},
            allowed_domains=["news.ycombinator.com", "techcrunch.com", "arstechnica.com"],
            save_browser_data=True,
            llm_model="gpt-4o",
            use_adblock=True,
            use_proxy=True,
            proxy_country_code="us",
            highlight_elements=True
        )
        print(f"Advanced task created with ID: {task_id}")
        
        # Get task details including live_url
        details = self.client.get_task_details(task_id)
        print(f"Live URL: {details.get('live_url', 'N/A')}")
        
        # Wait for completion
        result = self.monitor.wait_for_completion(task_id)
        print(f"Task completed!")
        
        # Get media files
        try:
            media = self.media_manager.get_task_media(task_id)
            print(f"Media files: {media}")
            
            screenshots = self.media_manager.get_task_screenshots(task_id)
            print(f"Screenshots: {screenshots}")
        except Exception as e:
            print(f"Could not retrieve media: {e}")

    def file_upload_example(self):
        """Example demonstrating file upload functionality"""
        try:
            # Get presigned URL for upload
            filename = "example.txt"
            upload_info = self.media_manager.get_presigned_upload_url(filename)
            print(f"Got presigned URL for {filename}")
            
            # Create a sample file
            with open("/tmp/example.txt", "w") as f:
                f.write("This is a sample file for testing uploads.")
            
            # Upload the file
            success = self.media_manager.upload_file_to_presigned_url(upload_info['presigned_url'], "/tmp/example.txt")
            if success:
                print("File uploaded successfully!")
                
                # Create task with uploaded file
                task_id = self.client.create_task(
                    "Analyze the content of the uploaded file and provide a summary",
                    included_file_names=[filename]
                )
                print(f"Task with file created: {task_id}")
            else:
                print("File upload failed")
        except Exception as e:
            print(f"Upload example failed: {e}")

    def run_all_demos(self):
        """Run all demonstration examples"""
        print("🚀 Browser Use API Demo Suite")
        print("=" * 50)
        
        # Validate API connection first
        if not ValidationUtils.validate_api_connection():
            print("❌ API validation failed. Please check your API key and connection.")
            return
        
        print("\n📋 Available API endpoints:")
        ValidationUtils.list_all_task_endpoints()
        
        # Initialize task manager
        task_manager = TaskManager()
        
        print("\n" + "=" * 50)
        print("=== Example 1: Basic Task ===")
        task_id = task_manager.create_and_track_task(
            'Open https://www.google.com and search for openai',
            task_name="Google Search"
        )
        
        print("\n=== Example 2: Structured Output Task ===")
        schema = SocialMediaCompanies.model_json_schema()
        structured_task_id = self.client.create_structured_task(
            "Get me the top social media companies by market cap",
            schema
        )
        print(f"Structured output task created: {structured_task_id}")
        
        print("\n=== Example 3: Advanced Task with Full Parameters ===")
        self.advanced_task_example()
        
        print("\n=== Example 4: Website Analysis Demo ===")
        special_creator = SpecializedTaskCreator()
        website_task_id = special_creator.create_website_analysis_task("https://www.example.com")
        print(f"Website analysis task created: {website_task_id}")
        
        print("\n=== Example 5: Batch News Collection Demo ===")
        batch_manager = BatchTaskManager()
        news_task_ids = batch_manager.create_batch_tasks([
            {'instructions': "Search for the latest AI news and summarize"},
            {'instructions': "Search for the latest tech industry news"}
        ])
        print(f"Created {len(news_task_ids)} batch news tasks")
        
        print("\n=== Example 6: Task Control (Interactive) ===")
        print("Skipping interactive control example. Uncomment in code to run.")
        # self.control_task_example()  # Uncomment to run interactively
        
        print("\n=== Example 7: File Upload ===")
        # self.file_upload_example()  # Uncomment to run file upload demo
        
        # Show task manager summary
        print("\n" + "=" * 50)
        print("📊 Task Manager Summary:")
        summary = task_manager.get_task_summary()
        print(f"Active tasks: {summary['active_count']}")
        print(f"Completed tasks: {summary['completed_count']}")
        
        if summary['active_tasks']:
            print("🔄 Monitoring active tasks...")
            task_manager.monitor_all_tasks()
        
        print("\n🎉 Demo completed! Check the individual methods for more examples.")
