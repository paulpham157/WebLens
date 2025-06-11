"""
Constants for Browser Use API

This module defines constants used throughout the Browser Use API client.
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API Configuration and Constants
BASE_URL = os.getenv("BROWSER_USE_BASE_URL") or "https://api.browser-use.com/api/v1"
API_KEY = os.getenv("BROWSER_USE_API_KEY") or "your_api_key_here"
HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}
