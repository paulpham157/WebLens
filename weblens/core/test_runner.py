"""
Test runner for WebLens
"""
import asyncio
from typing import List, Dict, Any, Optional, Callable, Union
from dataclasses import dataclass, field
from pathlib import Path
import time
import traceback
import json

from ..core.browser_manager import BrowserManager
from ..utils.logger import get_logger
from ..config import config

logger = get_logger(__name__)


@dataclass
class TestResult:
    """Test execution result"""
    name: str
    browser: str
    profile: Optional[str]
    status: str  # "passed", "failed", "skipped"
    duration: float
    error_message: Optional[str] = None
    screenshot_path: Optional[str] = None
    video_path: Optional[str] = None


@dataclass
class TestCase:
    """Test case definition"""
    name: str
    description: str
    test_function: Callable
    browsers: List[str] = field(default_factory=lambda: ["browser_use_cloud"])
    profiles: List[str] = field(default_factory=list)
    tags: List[str] = field(default_factory=list)


class TestRunner:
    """Main test runner for WebLens"""
    
    def __init__(self):
        self.browser_manager = BrowserManager()
        self.test_cases: List[TestCase] = []
        self.results: List[TestResult] = []
    
    def register_test(self, 
                     name: str, 
                     description: str,
                     test_function: Callable,
                     tags: Optional[List[str]] = None):
        """Register a test case"""
        test_case = TestCase(
            name=name,
            description=description,
            test_function=test_function,
            browsers=["browser_use_cloud"],  # Fixed value for cloud
            profiles=[],  # Not used in cloud mode
            tags=tags or []
        )
        self.test_cases.append(test_case)
        logger.info(f"Registered test: {name}")
    
    async def run_single_test(self, 
                            test_case: TestCase, 
                            task_description: Optional[str] = None) -> TestResult:
        """Run a single test case using browser-use cloud"""
        start_time = time.time()
        test_name = f"{test_case.name}_{int(start_time)}"
        
        logger.info(f"Running test: {test_name}")
        
        try:
            # Create agent for this test
            task = task_description or test_case.description or f"Execute test: {test_case.name}"
            agent = await self.browser_manager.create_agent(task, test_name)
            
            # Execute test function with agent
            if asyncio.iscoroutinefunction(test_case.test_function):
                await test_case.test_function(agent)
            else:
                test_case.test_function(agent)
            
            duration = time.time() - start_time
            result = TestResult(
                name=test_name,
                browser="browser_use_cloud",
                profile=None,
                status="passed",
                duration=duration
            )
            
            logger.info(f"Test passed: {test_name} ({duration:.2f}s)")
            
        except Exception as e:
            duration = time.time() - start_time
            error_message = f"{type(e).__name__}: {str(e)}"
            
            result = TestResult(
                name=test_name,
                browser="browser_use_cloud",
                profile=None,
                status="failed",
                duration=duration,
                error_message=error_message
            )
            
            logger.error(f"Test failed: {test_name} - {error_message}")
            logger.debug(f"Full traceback: {traceback.format_exc()}")
        
        finally:
            # Clean up agent
            try:
                await self.browser_manager.remove_agent(test_name)
            except:
                pass
        
        return result
    
    async def run_tests(self, 
                       test_names: Optional[List[str]] = None,
                       tags: Optional[List[str]] = None,
                       parallel: bool = False) -> List[TestResult]:
        """Run multiple tests using browser-use cloud"""
        logger.info("Starting test execution...")
        
        # Start browser manager
        await self.browser_manager.start()
        
        try:
            # Filter test cases
            tests_to_run = self._filter_tests(test_names, tags)
            
            if not tests_to_run:
                logger.warning("No tests to run")
                return []
            
            # Execute tests
            if parallel:
                logger.info(f"Running {len(tests_to_run)} tests in parallel...")
                tasks = [
                    asyncio.create_task(self.run_single_test(test_case))
                    for test_case in tests_to_run
                ]
                results = await asyncio.gather(*tasks, return_exceptions=True)
                
                for result in results:
                    if isinstance(result, Exception):
                        logger.error(f"Task execution error: {result}")
                    elif isinstance(result, TestResult):
                        self.results.append(result)
            else:
                logger.info(f"Running {len(tests_to_run)} tests sequentially...")
                for test_case in tests_to_run:
                    result = await self.run_single_test(test_case)
                    self.results.append(result)
            
            # Generate report
            await self._generate_report()
            
            logger.info(f"Test execution completed. {len(self.results)} tests run.")
            
        finally:
            # Stop browser manager
            await self.browser_manager.stop()
        
        return self.results
    
    def _filter_tests(self, 
                     test_names: Optional[List[str]] = None,
                     tags: Optional[List[str]] = None) -> List[TestCase]:
        """Filter tests based on criteria"""
        tests_to_run = []
        
        for test_case in self.test_cases:
            # Filter by test names
            if test_names and test_case.name not in test_names:
                continue
            
            # Filter by tags
            if tags and not any(tag in test_case.tags for tag in tags):
                continue
            
            tests_to_run.append(test_case)
        
        return tests_to_run
    
    async def _take_screenshot(self, browser, test_name: str) -> str:
        """Take screenshot for failed test"""
        timestamp = int(time.time())
        screenshot_path = config.screenshots_dir / f"{test_name}_{timestamp}.png"
        
        # Take screenshot using browser-use
        await browser.take_screenshot(str(screenshot_path))
        
        return str(screenshot_path)
    
    async def _generate_report(self):
        """Generate test execution report"""
        timestamp = int(time.time())
        report_path = config.reports_dir / f"test_report_{timestamp}.json"
        
        # Calculate summary
        total_tests = len(self.results)
        passed_tests = len([r for r in self.results if r.status == "passed"])
        failed_tests = len([r for r in self.results if r.status == "failed"])
        total_duration = sum(r.duration for r in self.results)
        
        report_data = {
            "summary": {
                "total_tests": total_tests,
                "passed": passed_tests,
                "failed": failed_tests,
                "success_rate": (passed_tests / total_tests * 100) if total_tests > 0 else 0,
                "total_duration": total_duration,
                "timestamp": timestamp
            },
            "results": [
                {
                    "name": r.name,
                    "browser": r.browser,
                    "profile": r.profile,
                    "status": r.status,
                    "duration": r.duration,
                    "error_message": r.error_message,
                    "screenshot_path": r.screenshot_path,
                    "video_path": r.video_path
                }
                for r in self.results
            ]
        }
        
        # Write report
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(report_data, f, indent=2, ensure_ascii=False)
        
        # Log summary
        logger.info(f"Test Summary:")
        logger.info(f"  Total: {total_tests}")
        logger.info(f"  Passed: {passed_tests}")
        logger.info(f"  Failed: {failed_tests}")
        logger.info(f"  Success Rate: {passed_tests / total_tests * 100:.1f}%" if total_tests > 0 else "  Success Rate: 0%")
        logger.info(f"  Duration: {total_duration:.2f}s")
        logger.info(f"  Report saved: {report_path}")


# Decorator for easy test registration
def weblens_test(name: str, 
                description: str = "",
                tags: Optional[List[str]] = None):
    """Decorator to register test functions"""
    def decorator(func):
        # This would typically be registered with a global test runner instance
        func._weblens_test_info = {
            "name": name,
            "description": description,
            "tags": tags
        }
        return func
    return decorator
