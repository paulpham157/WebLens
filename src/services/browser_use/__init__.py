"""
Browser Use API package provides a class-based interface to interact with the Browser Use API.
It allows you to run, pause, resume, and stop tasks using the API, as well as manage account information and balance.
"""
# Import constants first
from .constants import BASE_URL, API_KEY, HEADERS

# Import models before they're needed by other modules
from .models.models import (
    SocialMediaCompany, SocialMediaCompanies,
    WebsiteAnalysis, PriceComparison,
    PriceComparisonResults, NewsArticle,
    NewsCollection
)

# Now import core classes
from .api.client import BrowserUseClient
from .controllers.task_controller import TaskController
from .controllers.media_manager import MediaManager
from .controllers.task_monitor import TaskMonitor
from .controllers.batch_task_manager import BatchTaskManager
from .controllers.specialized_task_creator import SpecializedTaskCreator
from .controllers.task_manager import TaskManager
from .controllers.account_manager import AccountManager
from .utils.config import ConfigManager
from .utils.validation import ValidationUtils
from .utils.helpers import print_api_help, print_refactored_api_help
from .examples.examples import BrowserUseExamples
from .examples.account_examples import check_account_balance, get_account_details, get_usage_history

# Import legacy functions for backward compatibility
from .legacy import (
    create_task, create_structured_task,
    get_task_status, get_task_details,
    fetch_task_output, wait_for_task_completion,
    monitor_task_progress, stop_task,
    pause_task, resume_task,
    get_task_media, get_task_screenshots,
    get_task_gif, get_presigned_upload_url,
    upload_file_to_presigned_url
)

# Import constants
from .constants import BASE_URL, API_KEY, HEADERS

__all__ = [
    # Core Classes
    'BrowserUseClient', 'TaskController', 'MediaManager',
    'TaskMonitor', 'BatchTaskManager', 'SpecializedTaskCreator',
    'TaskManager', 'AccountManager', 'ConfigManager', 'ValidationUtils',
    'BrowserUseExamples',
    # Account Example Functions
    'check_account_balance', 'get_account_details', 'get_usage_history',
    
    # Models
    'SocialMediaCompany', 'SocialMediaCompanies',
    'WebsiteAnalysis', 'PriceComparison',
    'PriceComparisonResults', 'NewsArticle',
    'NewsCollection',
    
    # Helper Functions
    'print_api_help', 'print_refactored_api_help',
    
    # Legacy Functions
    'create_task', 'create_structured_task',
    'get_task_status', 'get_task_details',
    'fetch_task_output', 'wait_for_task_completion',
    'monitor_task_progress', 'stop_task',
    'pause_task', 'resume_task',
    'get_task_media', 'get_task_screenshots',
    'get_task_gif', 'get_presigned_upload_url',
    'upload_file_to_presigned_url',
    
    # Constants
    'BASE_URL', 'API_KEY', 'HEADERS'
]
