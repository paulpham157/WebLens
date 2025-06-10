"""
Browser Manager for WebLens using browser-use cloud
"""
import asyncio
from typing import Dict, Any, Optional
import logging

from ..config import config

logger = logging.getLogger(__name__)

# Try to import browser-use, with fallback for development
try:
    from browser_use import Agent as BrowserUseAgent
    # Define a type alias to avoid generic type issues
    Agent = BrowserUseAgent  # type: ignore
    BROWSER_USE_AVAILABLE = True
except ImportError:
    logger.warning("browser-use package not available. Using mock for development.")
    BROWSER_USE_AVAILABLE = False
    
    # Mock Agent class for development
    class Agent:
        def __init__(self, task: str, llm=None, **kwargs):
            self.task = task
            self.kwargs = kwargs
            logger.info(f"Mock Agent created for task: {task}")
        
        async def run(self):
            logger.info(f"Mock Agent running task: {self.task}")
            return "Mock result"
        
        async def screenshot(self, path: Optional[str] = None):
            logger.info(f"Mock screenshot saved to: {path}")
            return path


class BrowserManager:
    """Manages browser-use cloud agents for WebLens"""
    
    def __init__(self):
        self.agents: Dict[str, Agent] = {}
        self.is_started = False
        
    async def start(self):
        """Initialize browser manager"""
        if self.is_started:
            return
        
        # Validate configuration
        if not config.validate_config():
            if not BROWSER_USE_AVAILABLE:
                logger.warning("Running in mock mode - browser-use not available")
            else:
                raise ValueError("Invalid configuration. Check BROWSER_USE_API_KEY.")
        
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
        """Create a new browser-use agent"""
        if not self.is_started:
            await self.start()
        
        if agent_id is None:
            agent_id = f"agent_{len(self.agents)}"
        
        if agent_id in self.agents:
            logger.warning(f"Agent {agent_id} already exists, removing old one")
            await self.remove_agent(agent_id)
        
        if BROWSER_USE_AVAILABLE:
            # Create real browser-use agent
            browser_config = config.get_browser_use_config()
            agent = Agent(
                task=task,
                api_key=browser_config["api_key"],
                base_url=browser_config["base_url"]
            )
        else:
            # Create mock agent for development
            agent = Agent(task=task)
        
        self.agents[agent_id] = agent
        logger.info(f"Created agent {agent_id} for task: {task}")
        
        return agent
    
    async def get_agent(self, agent_id: str) -> Optional[Agent]:
        """Get existing agent by ID"""
        return self.agents.get(agent_id)
    
    async def remove_agent(self, agent_id: str):
        """Remove and clean up agent"""
        if agent_id in self.agents:
            agent = self.agents[agent_id]
            # Clean up agent if needed
            try:
                # Simple cleanup - just log removal
                pass
            except Exception as e:
                logger.warning(f"Error closing agent {agent_id}: {e}")
            
            del self.agents[agent_id]
            logger.info(f"Removed agent {agent_id}")
    
    async def list_agents(self) -> Dict[str, str]:
        """List all active agents"""
        return {
            agent_id: getattr(agent, 'task', 'Unknown task')
            for agent_id, agent in self.agents.items()
        }
    
    def get_stats(self) -> Dict[str, Any]:
        """Get browser manager statistics"""
        return {
            "active_agents": len(self.agents),
            "is_started": self.is_started,
            "browser_use_available": BROWSER_USE_AVAILABLE
        }