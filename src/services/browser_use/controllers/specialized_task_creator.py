"""
Specialized Task Creator for Browser Use API

This module provides specialized task creation functionality for Browser Use API.
"""
from typing import Dict, Any, Optional, List

from ..constants import BASE_URL, API_KEY
from ..api.client import BrowserUseClient
from ..utils.config import ConfigManager
from ..models.models import WebsiteAnalysis, PriceComparisonResults, NewsCollection

class SpecializedTaskCreator:
    """Create tasks for specific use cases with optimized configurations"""
    
    def __init__(self, base_url: Optional[str] = None, api_key: Optional[str] = None):
        self.base_url = base_url or BASE_URL
        self.api_key = api_key or API_KEY
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        self.client = BrowserUseClient(self.base_url, self.api_key)
        self.config_manager = ConfigManager()
    
    def create_website_analysis_task(self, url: str, **kwargs) -> str:
        """
        Create a task specifically for website analysis
        
        Args:
            url: Website URL to analyze
            **kwargs: Additional task parameters
            
        Returns:
            Task ID
        """
        schema = WebsiteAnalysis.model_json_schema()
        instructions = f"Analyze the website at {url}. Provide title, meta description, main content summary, count of links and images, estimated load time, and accessibility score (1-100)."
        
        # Get optimized config for web scraping
        config = self.config_manager.get_config_for_task_type('web_scraping')
        
        # Override with any custom configs
        for key, value in kwargs.items():
            config[key] = value
            
        return self.client.create_structured_task(instructions, schema, **config)
    
    def create_price_comparison_task(self, product_name: str, stores: Optional[List[str]] = None, **kwargs) -> str:
        """
        Create a task for price comparison across multiple stores
        
        Args:
            product_name: Product to search for
            stores: Optional list of store names
            **kwargs: Additional task parameters
            
        Returns:
            Task ID
        """
        schema = PriceComparisonResults.model_json_schema()
        
        stores_text = f" from {', '.join(stores)}" if stores else ""
        instructions = f"Search for '{product_name}'{stores_text} and compare prices. Include product name, price, currency, store name, availability status, and rating if available."
        
        # Set up allowed domains if stores specified
        if stores:
            kwargs['allowed_domains'] = [store.lower().replace(' ', '') + '.com' for store in stores]
        
        # Get optimized config for ecommerce
        config = self.config_manager.get_config_for_task_type('ecommerce')
        
        # Override with any custom configs
        for key, value in kwargs.items():
            config[key] = value
            
        return self.client.create_structured_task(instructions, schema, **config)
    
    def create_news_collection_task(self, topic: str, max_articles: int = 5, **kwargs) -> str:
        """
        Create a task for collecting news articles on a specific topic
        
        Args:
            topic: News topic to search for
            max_articles: Maximum number of articles to collect
            **kwargs: Additional task parameters
            
        Returns:
            Task ID
        """
        schema = NewsCollection.model_json_schema()
        instructions = f"Search for the latest {max_articles} news articles about '{topic}'. For each article, provide title, summary, author, published date, source, and category."
        
        # Common news domains
        kwargs.setdefault('allowed_domains', [
            'bbc.com', 'cnn.com', 'reuters.com', 'techcrunch.com', 
            'arstechnica.com', 'theverge.com', 'news.ycombinator.com'
        ])
        
        # Get optimized config
        config = self.config_manager.get_config_for_task_type('web_scraping')
        
        # Override with any custom configs
        for key, value in kwargs.items():
            config[key] = value
            
        return self.client.create_structured_task(instructions, schema, **config)
