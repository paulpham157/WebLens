#!/usr/bin/env python3
"""
Direct browser-use example using natural language instructions
"""
import os
import json
import time
import asyncio
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get API key from environment variables
API_KEY = os.getenv('BROWSER_USE_API_KEY')
if not API_KEY:
    raise ValueError("BROWSER_USE_API_KEY not found in environment variables")

BASE_URL = 'https://api.browser-use.com/api/v1'
HEADERS = {'Authorization': f'Bearer {API_KEY}'}


def create_task(instructions: str):
    """Create a new browser automation task"""
    print(f"Creating task with instructions: {instructions}")
    response = requests.post(f'{BASE_URL}/run-task', headers=HEADERS, json={'task': instructions})
    task_id = response.json()['id']
    print(f"Task created with ID: {task_id}")
    return task_id


def get_task_status(task_id: str):
    """Get current task status"""
    response = requests.get(f'{BASE_URL}/task/{task_id}/status', headers=HEADERS)
    return response.json()


def get_task_details(task_id: str):
    """Get full task details including output"""
    response = requests.get(f'{BASE_URL}/task/{task_id}', headers=HEADERS)
    return response.json()


def wait_for_completion(task_id: str, poll_interval: int = 2):
    """Poll task status until completion"""
    print(f"Waiting for task {task_id} to complete...")
    count = 0
    unique_steps = []
    
    while True:
        details = get_task_details(task_id)
        new_steps = details['steps']
        
        # Print only new steps
        if new_steps != unique_steps:
            for step in new_steps[len(unique_steps):]:
                print(json.dumps(step, indent=4))
            unique_steps = new_steps
        
        count += 1
        status = details['status']

        if status in ['finished', 'failed', 'stopped']:
            print(f"Task {status}.")
            return details
            
        time.sleep(poll_interval)


def run_test_scenario(instructions: str):
    """Run a test scenario with natural language instructions"""
    task_id = create_task(instructions)
    task_details = wait_for_completion(task_id)
    
    print("\n--- Task Results ---")
    print(f"Status: {task_details['status']}")
    print(f"Output: {task_details['output']}")
    
    # Optional: save screenshot if available
    if 'screenshot' in task_details and task_details['screenshot']:
        screenshot_url = task_details['screenshot']
        print(f"Screenshot available at: {screenshot_url}")
    
    return task_details


# Example test scenarios using natural language
TEST_SCENARIOS = [
    "Go to example.com, check if the page title contains 'Example', and take a screenshot",
    
    "Go to httpbin.org/forms/post, fill out the customer name as 'Test User', " 
    "phone as '123-456-7890', email as 'test@example.com', select 'large' size, "
    "submit the form, and verify the response contains the submitted data",
    
    "Go to google.com, search for 'WebLens testing framework', wait for search results, "
    "and check if there are at least 5 search results on the page"
]


def main():
    """Run all test scenarios"""
    for i, instructions in enumerate(TEST_SCENARIOS):
        print(f"\n=== Running Test Scenario {i+1} ===")
        try:
            run_test_scenario(instructions)
            print(f"✅ Test scenario {i+1} completed")
        except Exception as e:
            print(f"❌ Test scenario {i+1} failed: {e}")
        print("="*50)


if __name__ == "__main__":
    main()
