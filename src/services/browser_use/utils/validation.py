"""
Validation Utilities for Browser Use API

This module provides validation functionality for Browser Use API.
"""
import requests
from typing import Dict, Any, Optional

from ..constants import BASE_URL, API_KEY

class ValidationUtils:
    """Utilities for API validation and error handling"""
    
    @staticmethod
    def validate_api_connection() -> bool:
        """Validate API connection and credentials"""
        try:
            print("🔍 Validating API connection...")
            
            # Check if API key is configured
            if API_KEY == "your_api_key_here" or not API_KEY:
                print("❌ API key not configured. Please set BROWSER_USE_API_KEY environment variable.")
                return False
            
            # Import client here to avoid circular imports
            from ..api.client import BrowserUseClient
            
            # Try to create a simple test task to validate credentials
            client = BrowserUseClient()
            test_task_id = client.create_task("Simple validation test - just return 'API connection successful'")
            print(f"✅ API connection successful! Test task ID: {test_task_id}")
            
            # Stop the test task immediately to avoid unnecessary usage
            try:
                # Import controller here to avoid circular imports
                from ..controllers.task_controller import TaskController
                controller = TaskController()
                controller.stop_task(test_task_id)
                print("✅ Test task stopped successfully")
            except Exception as e:
                print(f"⚠️ Could not stop test task, but API connection is working: {e}")
            
            return True
        except Exception as e:
            print(f"❌ API connection failed: {e}")
            if "401" in str(e) or "Unauthorized" in str(e):
                print("💡 Hint: Check your API key in the .env file")
            elif "403" in str(e) or "Forbidden" in str(e):
                print("💡 Hint: Your API key might not have the required permissions")
            elif "404" in str(e):
                print("💡 Hint: Check the BASE_URL configuration")
            return False
    
    @staticmethod
    def handle_api_error(response: requests.Response, context: str = "API call") -> bool:
        """Enhanced error handling for API responses"""
        if response.status_code == 200:
            return True
        
        error_messages = {
            400: "Bad Request - Check your parameters",
            401: "Unauthorized - Check your API key", 
            403: "Forbidden - Insufficient permissions",
            404: "Not Found - Check the endpoint URL",
            429: "Rate Limited - Too many requests",
            500: "Server Error - Try again later",
            503: "Service Unavailable - API is down"
        }
        
        error_msg = error_messages.get(response.status_code, f"HTTP {response.status_code}")
        print(f"❌ {context} failed: {error_msg}")
        
        try:
            error_detail = response.json()
            if 'detail' in error_detail:
                print(f"   Details: {error_detail['detail']}")
            elif 'message' in error_detail:
                print(f"   Message: {error_detail['message']}")
        except:
            print(f"   Response: {response.text[:200]}")
        
        return False
    
    @staticmethod
    def check_api_status() -> bool:
        """Check API service status"""
        try:
            # Simple health check - try to access the base URL
            response = requests.get(f"{BASE_URL.replace('/api/v1', '')}", timeout=10)
            if response.status_code == 200:
                print("✅ Browser Use API service is online")
                return True
            else:
                print(f"⚠️ API service returned status code: {response.status_code}")
                return False
        except requests.exceptions.ConnectionError:
            print("❌ Cannot connect to Browser Use API service")
            return False
        except requests.exceptions.Timeout:
            print("⏰ API service connection timed out")
            return False
        except Exception as e:
            print(f"❌ Error checking API status: {e}")
            return False
    
    @staticmethod
    def list_all_task_endpoints():
        """Display all available API endpoints for reference"""
        endpoints = {
            "🎯 Task Management": [
                f"POST {BASE_URL}/run-task - Create a new task",
                f"GET {BASE_URL}/task/{{task_id}} - Get task details",
                f"GET {BASE_URL}/task/{{task_id}}/status - Get task status",
                f"PUT {BASE_URL}/pause-task?task_id={{task_id}} - Pause task",
                f"PUT {BASE_URL}/resume-task?task_id={{task_id}} - Resume task", 
                f"PUT {BASE_URL}/stop-task?task_id={{task_id}} - Stop task"
            ],
            "📁 Media & Files": [
                f"GET {BASE_URL}/task/{{task_id}}/media - Get task recordings",
                f"GET {BASE_URL}/task/{{task_id}}/screenshots - Get task screenshots",
                f"GET {BASE_URL}/task/{{task_id}}/gif - Get task GIF",
                f"POST {BASE_URL}/uploads/presigned-url - Get upload URL"
            ]
        }
        
        print("🌐 Browser Use API Endpoints:")
        for category, endpoints_list in endpoints.items():
            print(f"\n{category}:")
            for endpoint in endpoints_list:
                print(f"  • {endpoint}")
