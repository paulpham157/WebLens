"""
Unit tests for WebLens BrowserManager with browser-use cloud API
"""
import pytest
import asyncio
from unittest.mock import Mock, AsyncMock, patch
from pathlib import Path

from weblens.core.browser_manager import BrowserManager, Agent, BROWSER_USE_AVAILABLE


class TestBrowserManager:
    """Test cases for cloud-based BrowserManager"""
    
    @pytest.mark.asyncio
    async def test_browser_manager_initialization(self):
        """Test browser manager initialization"""
        manager = BrowserManager()
        assert manager.agents == {}
        assert manager.is_started == False
    
    @pytest.mark.asyncio
    async def test_browser_manager_start_stop(self):
        """Test browser manager start and stop"""
        manager = BrowserManager()
        
        # Start browser manager
        await manager.start()
        assert manager.is_started == True
        
        # Stop browser manager
        await manager.stop()
        assert manager.is_started == False
    
    @pytest.mark.asyncio
    async def test_create_agent(self):
        """Test agent creation"""
        manager = BrowserManager()
        await manager.start()
        
        try:
            # Create agent
            agent = await manager.create_agent("Test task", "test_agent")
            
            # Verify agent was created
            assert "test_agent" in manager.agents
            assert agent is not None
            
            # Get agent
            retrieved_agent = await manager.get_agent("test_agent")
            assert retrieved_agent is agent
            
            # List agents
            agents = await manager.list_agents()
            assert "test_agent" in agents
            assert agents["test_agent"] == "Test task"
            
            # Get stats
            stats = manager.get_stats()
            assert stats["active_agents"] == 1
            assert stats["is_started"] == True
            assert stats["browser_use_available"] == BROWSER_USE_AVAILABLE
            
        finally:
            # Clean up
            await manager.stop()
    
    @pytest.mark.asyncio
    async def test_remove_agent(self):
        """Test agent removal"""
        manager = BrowserManager()
        await manager.start()
        
        try:
            # Create and remove agent
            agent = await manager.create_agent("Test task", "test_agent")
            assert "test_agent" in manager.agents
            
            await manager.remove_agent("test_agent")
            assert "test_agent" not in manager.agents
            
        finally:
            # Clean up
            await manager.stop()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
