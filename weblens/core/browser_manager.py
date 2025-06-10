"""
Browser Manager for WebLens using browser-use cloud with direct natural language instructions
"""
import asyncio
import os
import json
import time
import requests
from typing import Dict, Any, Optional, List, Union
import logging
from pathlib import Path
import re

from ..config import config

logger = logging.getLogger(__name__)

# Flag to check if browser-use is available
BROWSER_USE_AVAILABLE = True

# Define a custom Agent class that uses the browser-use REST API directly
class Agent:
    """Agent class for browser-use cloud API using direct natural language instructions"""
    
    def __init__(self, task: str, api_key: Optional[str] = None, base_url: Optional[str] = None, **kwargs):
        """Initialize a new agent with the given task"""
        self.task = task
        api_key_env = os.getenv('BROWSER_USE_API_KEY')
        if not api_key and not api_key_env:
            raise ValueError("BROWSER_USE_API_KEY not found. Please set it in your environment variables.")
        
        self.api_key = api_key or api_key_env
        self.base_url = base_url or os.getenv('BROWSER_USE_BASE_URL') or 'https://api.browser-use.com/api/v1'
        self.headers = {'Authorization': f'Bearer {self.api_key}'}
        self.kwargs = kwargs
        self.task_id = None
        self.status = None
        self.output = None
        self.steps = []
        self.screenshot_url = None
        self.error = None
        self.result_data = {}
        
        # Validate the task instructions
        self._validate_instructions(task)
        logger.info(f"Agent created for task: {task}")
    
    def _validate_instructions(self, instructions: str) -> bool:
        """Validate natural language instructions for common issues"""
        if not instructions or not instructions.strip():
            raise ValueError("Task instructions cannot be empty")
        
        if len(instructions) < 10:
            logger.warning("Task instructions are very short, might not be descriptive enough")
            
        if len(instructions) > 2000:
            logger.warning("Task instructions are very long, consider simplifying")
        
        # Check for common code fragments that should be natural language instead
        code_patterns = [
            r'\.click\(', r'\.navigate\(', r'\.goto\(', r'\.fill\(', 
            r'await page\.', r'driver\.', r'selenium\.', r'playwright\.'
        ]
        
        for pattern in code_patterns:
            if re.search(pattern, instructions):
                logger.warning(f"Detected possible code fragment in natural language instructions: {pattern}")
                logger.warning("Please use natural language instead of code syntax in task descriptions")
        
        return True
    
    async def run(self):
        """Run the agent's task using natural language instructions"""
        if not self.api_key:
            raise ValueError("BROWSER_USE_API_KEY not found. Please set it in your environment variables.")
        
        self.error = None
        try:
            # Create the task
            logger.info(f"Running natural language task: {self.task}")
            response = requests.post(
                f'{self.base_url}/run-task',
                headers=self.headers,
                json={'task': self.task, **self.kwargs}
            )
            
            if response.status_code >= 400:
                error_detail = response.json() if response.content else "No details available"
                self.error = f"API error ({response.status_code}): {error_detail}"
                logger.error(self.error)
                raise ValueError(self.error)
            
            self.task_id = response.json()['id']
            logger.info(f"Task created with ID: {self.task_id}")
            
            # Wait for task completion
            result = await self._wait_for_completion()
            self.output = result.get('output')
            self.screenshot_url = result.get('screenshot')
            self.result_data = result
            
            if self.status == "failed":
                self.error = result.get("error") or "Task failed without specific error"
                logger.error(f"Task failed: {self.error}")
                raise ValueError(f"Task execution failed: {self.error}")
            
            logger.info(f"Task completed successfully")
            return self.output
        
        except requests.RequestException as e:
            self.error = f"Network error: {str(e)}"
            logger.error(self.error)
            raise ValueError(self.error)
        except Exception as e:
            if not self.error:
                self.error = f"Error executing task: {str(e)}"
                logger.error(self.error)
            raise ValueError(self.error)
    
    async def _wait_for_completion(self, poll_interval: int = 2):
        """Poll task status until completion"""
        logger.info(f"Waiting for task {self.task_id} to complete...")
        
        while True:
            details = self._get_task_details()
            new_steps = details.get('steps', [])
            
            # Log new steps
            if new_steps != self.steps:
                for step in new_steps[len(self.steps):]:
                    logger.info(f"Task step: {json.dumps(step)}")
                self.steps = new_steps
            
            self.status = details.get('status')
            
            if self.status in ['finished', 'failed', 'stopped']:
                logger.info(f"Task {self.task_id} {self.status}.")
                return details
            
            await asyncio.sleep(poll_interval)
    
    def _get_task_details(self):
        """Get full task details including output"""
        response = requests.get(f'{self.base_url}/task/{self.task_id}', headers=self.headers)
        response.raise_for_status()
        return response.json()
    
    async def take_screenshot(self, path: Optional[str] = None):
        """Save screenshot from the completed task"""
        if not self.screenshot_url:
            logger.warning("No screenshot available")
            return None
        
        if not path:
            # Generate a path if none provided
            screenshots_dir = config.screenshots_dir
            path = str(screenshots_dir / f"{self.task_id}_{int(time.time())}.png")
        
        # Ensure directories exist
        os.makedirs(os.path.dirname(path), exist_ok=True)
        
        # Download the screenshot
        try:
            response = requests.get(self.screenshot_url)
            response.raise_for_status()
            
            with open(path, 'wb') as f:
                f.write(response.content)
            
            logger.info(f"Screenshot saved to: {path}")
            return path
        except Exception as e:
            logger.error(f"Error saving screenshot: {e}")
            return None
            
    async def execute_natural_language(self, instructions: str):
        """Execute additional instructions using natural language"""
        # Create a new task with the additional instructions
        original_task = self.task
        self.task = instructions
        result = await self.run()
        self.task = original_task  # Restore original task description
        return result
        
    def get_last_step_details(self) -> Dict[str, Any]:
        """Get details of the last step executed"""
        if not self.steps:
            return {}
        return self.steps[-1]
    
    def get_execution_summary(self) -> Dict[str, Any]:
        """Get a summary of the execution"""
        return {
            "task": self.task,
            "task_id": self.task_id,
            "status": self.status,
            "output": self.output,
            "error": self.error,
            "has_screenshot": bool(self.screenshot_url),
            "step_count": len(self.steps)
        }


class BrowserManager:
    """Manages browser-use cloud agents for WebLens using direct natural language instructions"""
    
    def __init__(self):
        self.agents: Dict[str, Agent] = {}
        self.is_started = False
        
    async def start(self):
        """Initialize browser manager"""
        if self.is_started:
            return
        
        # Validate configuration
        api_key = os.getenv('BROWSER_USE_API_KEY')
        if not api_key:
            logger.warning("BROWSER_USE_API_KEY not found in environment variables")
            raise ValueError("Invalid configuration. Set BROWSER_USE_API_KEY in your environment.")
        
        self.is_started = True
        logger.info("BrowserManager started")
    
    async def stop(self):
        """Clean up browser manager"""
        if not self.is_started:
            return
        
        # Clean up all agents
        for agent_id in list(self.agents.keys()):
            await self.remove_agent(agent_id)
        
        self.is_started = False
        logger.info("BrowserManager stopped")
    
    async def create_agent(self, task: str, agent_id: Optional[str] = None) -> Agent:
        """Create a new browser-use agent with natural language instructions"""
        if not self.is_started:
            await self.start()
        
        if agent_id is None:
            agent_id = f"agent_{len(self.agents)}"
        
        if agent_id in self.agents:
            logger.warning(f"Agent {agent_id} already exists, removing old one")
            await self.remove_agent(agent_id)
        
        # Create agent with natural language instructions
        try:
            agent = Agent(task=task)
            self.agents[agent_id] = agent
            logger.info(f"Created agent {agent_id} for task: {task}")
            return agent
        except Exception as e:
            logger.error(f"Failed to create agent: {e}")
            raise
    
    async def get_agent(self, agent_id: str) -> Optional[Agent]:
        """Get existing agent by ID"""
        return self.agents.get(agent_id)
    
    async def remove_agent(self, agent_id: str):
        """Remove and clean up agent"""
        if agent_id in self.agents:
            agent = self.agents[agent_id]
            # No complex cleanup needed for REST API approach
            
            del self.agents[agent_id]
            logger.info(f"Removed agent {agent_id}")
    
    async def list_agents(self) -> Dict[str, str]:
        """List all active agents"""
        return {
            agent_id: agent.task
            for agent_id, agent in self.agents.items()
        }
    
    def get_stats(self) -> Dict[str, Any]:
        """Get browser manager statistics"""
        return {
            "active_agents": len(self.agents),
            "is_started": self.is_started,
            "browser_use_available": BROWSER_USE_AVAILABLE
        }