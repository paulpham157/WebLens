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
import textwrap


# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from weblens import BrowserManager, TestRunner, ProfileManager
from weblens.utils.logger import setup_logging, get_logger
from weblens.config import config

# Constants for natural language templates
NATURAL_LANGUAGE_TEMPLATE = """#!/usr/bin/env python3
\"\"\"
WebLens Natural Language Test Example
\"\"\"
import asyncio
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from weblens.core.test_runner import weblens_test, TestRunner
from weblens.utils.logger import setup_logging, get_logger

# Setup logging
setup_logging(level="INFO")
logger = get_logger(__name__)


@weblens_test(
    name="{test_name}",
    description="{test_description}",
    tags=[{tags}]
)
async def test_natural_language(browser):
    \"\"\"Test using natural language instructions\"\"\"
    result = await browser.run()
    logger.info(f"Test result: {{result}}")
    
    # Add your assertions here
    assert result, "Test should return a result"


async def main():
    \"\"\"Main function to run tests\"\"\"
    runner = TestRunner()
    
    # Register test function
    info = test_natural_language._weblens_test_info
    runner.register_test(
        name=info["name"],
        description=info["description"],
        test_function=test_natural_language,
        tags=info["tags"]
    )
    
    try:
        logger.info(f"Running test: {{info['name']}}")
        results = await runner.run_tests(
            test_names=[info["name"]],
            parallel=False
        )
        
        # Print summary
        passed = len([r for r in results if r.status == "passed"])
        failed = len([r for r in results if r.status == "failed"])
        logger.info(f"Tests completed: {{passed}} passed, {{failed}} failed")
        
    except Exception as e:
        logger.error(f"Error running tests: {{e}}")
        raise


if __name__ == "__main__":
    asyncio.run(main())
"""


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


def generate_natural_language_test(test_name: str, test_description: str, output_path: str, tags: Optional[List[str]] = None):
    """Generate a natural language test template"""
    logger = get_logger(__name__)
    
    if not test_name:
        raise ValueError("Test name is required")
    if not test_description:
        raise ValueError("Test description is required")
    if not output_path:
        raise ValueError("Output path is required")
    
    # Format tags for template
    tags_str = ', '.join([f'"{tag}"' for tag in tags]) if tags else '"natural-language"'
    
    # Generate content from template
    content = NATURAL_LANGUAGE_TEMPLATE.format(
        test_name=test_name,
        test_description=test_description,
        tags=tags_str
    )
    
    # Ensure path has .py extension
    if not output_path.endswith('.py'):
        output_path += '.py'
    
    # Write to file
    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_file, 'w') as f:
        f.write(content)
    
    # Make file executable
    output_file.chmod(output_file.stat().st_mode | 0o111)  # Add execute permission
    
    logger.info(f"Generated natural language test template: {output_file}")
    print(f"✅ Natural language test template generated: {output_file}")
    return output_path


def generate_test_interactive():
    """Interactive natural language test generation"""
    print("Generate Natural Language Test")
    print("=" * 30)
    
    test_name = input("Test name: ").strip()
    if not test_name:
        print("Test name is required")
        return
    
    print("\nEnter test description (natural language instructions for the browser):")
    print("Example: Go to example.com, check the page title, and click on the first link")
    test_description = input("> ").strip()
    if not test_description:
        print("Test description is required")
        return
    
    tags_input = input("\nTags (comma-separated, optional): ").strip()
    tags = [tag.strip() for tag in tags_input.split(',')] if tags_input else []
    
    default_path = f"nl_test_{test_name.lower().replace(' ', '_')}.py"
    output_path = input(f"\nOutput file path (default: {default_path}): ").strip() or default_path
    
    try:
        generate_natural_language_test(test_name, test_description, output_path, tags)
    except Exception as e:
        print(f"Error generating test: {e}")


def main():
    """Main CLI function"""
    parser = argparse.ArgumentParser(
        description="WebLens - Advanced Web Testing Framework with Natural Language",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent("""
        Examples:
          weblens run examples/basic_tests.py
          weblens run tests/ --parallel
          weblens run tests/ --tags smoke
          weblens generate --name "Login Test" --description "Go to example.com/login, enter username and password, click login"
          weblens generate interactive
          weblens profiles list
          weblens profiles create
        """)
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Run command
    run_parser = subparsers.add_parser('run', help='Run tests')
    run_parser.add_argument('path', help='Path to test file or directory')
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
    run_parser.add_argument('--natural-language', action='store_true',
                           help='Flag to indicate this is a direct natural language test')
    run_parser.add_argument('--description',
                           help='Natural language description for the test (requires --natural-language)')
    
    # Generate command
    generate_parser = subparsers.add_parser('generate', help='Generate natural language test templates')
    generate_subparsers = generate_parser.add_subparsers(dest='generate_command')
    
    # Interactive generation
    generate_subparsers.add_parser('interactive', help='Generate test template interactively')
    
    # Direct generation
    direct_gen_parser = generate_subparsers.add_parser('template', help='Generate test template with parameters')
    direct_gen_parser.add_argument('--name', required=True, help='Test name')
    direct_gen_parser.add_argument('--description', required=True, help='Natural language test description')
    direct_gen_parser.add_argument('--output', required=True, help='Output file path')
    direct_gen_parser.add_argument('--tags', nargs='+', help='Optional tags for the test')
    
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
    
    elif args.command == 'generate':
        if args.generate_command == 'interactive':
            generate_test_interactive()
        elif args.generate_command == 'template':
            try:
                generate_natural_language_test(
                    test_name=args.name,
                    test_description=args.description,
                    output_path=args.output,
                    tags=args.tags
                )
            except Exception as e:
                print(f"Error generating test: {e}")
                sys.exit(1)
        else:
            parser.parse_args(['generate', '--help'])


if __name__ == "__main__":
    main()
