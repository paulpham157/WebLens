#!/usr/bin/env python3
"""
WebLens CLI - Command line interface for WebLens testing framework
"""
import argparse
import asyncio
import sys
from pathlib import Path
import importlib.util
from typing import Union, Optional, List


# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from weblens import BrowserManager, TestRunner, ProfileManager
from weblens.utils.logger import setup_logging, get_logger
from weblens.config import config


def load_test_module(module_path: Union[str, Path]):
    """Load test module from file path"""
    module_path = Path(module_path)
    if not module_path.exists():
        raise FileNotFoundError(f"Test module not found: {module_path}")
    
    spec = importlib.util.spec_from_file_location("test_module", module_path)
    if spec is None:
        raise ImportError(f"Could not create module spec from {module_path}")
    
    if spec.loader is None:
        raise ImportError(f"Module loader is None for {module_path}")
        
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


async def run_tests_from_module(module_path: str, 
                               browsers: Optional[List[str]] = None,
                               profiles: Optional[List[str]] = None,
                               tags: Optional[List[str]] = None,
                               parallel: bool = True,
                               test_names: Optional[List[str]] = None):
    """Run tests from a Python module"""
    logger = get_logger(__name__)
    
    # Load test module
    try:
        module = load_test_module(module_path)
        logger.info(f"Loaded test module: {module_path}")
    except Exception as e:
        logger.error(f"Failed to load test module {module_path}: {e}")
        return False
    
    # Create test runner
    runner = TestRunner()
    
    # Find and register test functions
    test_count = 0
    for attr_name in dir(module):
        attr = getattr(module, attr_name)
        if callable(attr) and hasattr(attr, '_weblens_test_info'):
            info = attr._weblens_test_info
            runner.register_test(
                name=info['name'],
                description=info['description'],
                test_function=attr,
                tags=info.get('tags')
            )
            test_count += 1
    
    logger.info(f"Registered {test_count} tests from module")
    
    if test_count == 0:
        logger.warning("No tests found in module")
        return False
    
    # Run tests
    try:
        results = await runner.run_tests(
            test_names=test_names,
            tags=tags,
            parallel=parallel
        )
        
        # Return success if all tests passed
        return all(r.status == "passed" for r in results)
    
    except Exception as e:
        logger.error(f"Test execution failed: {e}")
        return False


async def list_profiles(browser: Optional[str] = None):
    """List available profiles"""
    profile_manager = ProfileManager()
    profiles = profile_manager.list_profiles(browser)
    
    print("Available Profiles:")
    print("=" * 50)
    
    if not profiles:
        print("No profiles found")
        return
    
    for profile in profiles:
        print(f"Name: {profile.name}")
        print(f"Browser: {profile.browser}")
        if profile.viewport:
            print(f"Viewport: {profile.viewport['width']}x{profile.viewport['height']}")
        if profile.user_agent:
            print(f"User Agent: {profile.user_agent[:60]}...")
        print("-" * 30)


async def create_profile_interactive():
    """Interactive profile creation"""
    profile_manager = ProfileManager()
    
    print("Create New Browser Profile")
    print("=" * 30)
    
    name = input("Profile name: ").strip()
    if not name:
        print("Profile name is required")
        return
    
    print("Available browsers: chrome, firefox, safari, edge")
    browser = input("Browser: ").strip().lower()
    if browser not in ["chrome", "firefox", "safari", "edge"]:
        print("Invalid browser")
        return
    
    # Optional settings
    print("\nOptional settings (press Enter to skip):")
    
    user_agent = input("User Agent: ").strip() or None
    
    try:
        width = input("Viewport width (default 1920): ").strip()
        width = int(width) if width else 1920
        
        height = input("Viewport height (default 1080): ").strip()
        height = int(height) if height else 1080
        
        viewport = {"width": width, "height": height}
    except ValueError:
        viewport = {"width": 1920, "height": 1080}
    
    locale = input("Locale (default en-US): ").strip() or "en-US"
    timezone = input("Timezone (default America/New_York): ").strip() or "America/New_York"
    
    # Create profile
    profile = profile_manager.create_profile(
        name=name,
        browser=browser,
        user_agent=user_agent,
        viewport=viewport,
        locale=locale,
        timezone=timezone
    )
    
    print(f"\nProfile '{name}' created successfully!")
    print(f"Browser: {profile.browser}")
    if profile.viewport:
        print(f"Viewport: {profile.viewport['width']}x{profile.viewport['height']}")


def main():
    """Main CLI function"""
    parser = argparse.ArgumentParser(
        description="WebLens - Advanced Web Testing Framework",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  weblens run examples/basic_tests.py
  weblens run tests/ --browsers chrome firefox --parallel
  weblens run tests/ --tags smoke --profiles desktop_chrome
  weblens profiles list
  weblens profiles create
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Run command
    run_parser = subparsers.add_parser('run', help='Run tests')
    run_parser.add_argument('path', help='Path to test file or directory')
    run_parser.add_argument('--browsers', nargs='+', default=['chrome'],
                           choices=['chrome', 'firefox', 'safari', 'edge'],
                           help='Browsers to test (default: chrome)')
    run_parser.add_argument('--profiles', nargs='+',
                           help='Profiles to use (default: all available)')
    run_parser.add_argument('--tags', nargs='+',
                           help='Filter tests by tags')
    run_parser.add_argument('--tests', nargs='+',
                           help='Specific test names to run')
    run_parser.add_argument('--parallel', action='store_true', default=True,
                           help='Run tests in parallel (default: True)')
    run_parser.add_argument('--sequential', action='store_true',
                           help='Run tests sequentially')
    run_parser.add_argument('--log-level', default='INFO',
                           choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'],
                           help='Log level (default: INFO)')
    
    # Profiles command
    profiles_parser = subparsers.add_parser('profiles', help='Manage browser profiles')
    profiles_subparsers = profiles_parser.add_subparsers(dest='profiles_command')
    
    # List profiles
    list_profiles_parser = profiles_subparsers.add_parser('list', help='List profiles')
    list_profiles_parser.add_argument('--browser',
                                     choices=['chrome', 'firefox', 'safari', 'edge'],
                                     help='Filter by browser')
    
    # Create profile
    profiles_subparsers.add_parser('create', help='Create new profile interactively')
    
    # Parse arguments
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    # Setup logging
    setup_logging(level=getattr(args, 'log_level', 'INFO'))
    
    if args.command == 'run':
        # Determine parallel mode
        parallel = args.parallel and not args.sequential
        
        # Run tests
        success = asyncio.run(run_tests_from_module(
            module_path=args.path,
            browsers=args.browsers,
            profiles=args.profiles,
            tags=args.tags,
            test_names=args.tests,
            parallel=parallel
        ))
        
        sys.exit(0 if success else 1)
    
    elif args.command == 'profiles':
        if args.profiles_command == 'list':
            asyncio.run(list_profiles(args.browser))
        elif args.profiles_command == 'create':
            asyncio.run(create_profile_interactive())
        else:
            profiles_parser.print_help()


if __name__ == "__main__":
    main()
