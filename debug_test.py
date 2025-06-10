#!/usr/bin/env python3
"""
Very basic test with natural language
"""
import asyncio
import sys
print("Starting test...")
sys.stdout.flush()

try:
    from weblens.core.test_runner import TestRunner
    print("TestRunner imported successfully")
    
    async def test_func(agent):
        print("Test function called")
        # Using natural language approach
        result = await agent.execute_natural_language("Check if the test setup is working correctly")
        print(f"Natural language result: {result}")
        return True
    
    async def main():
        print("Creating runner...")
        runner = TestRunner()
        print("Runner created")
        
        print("Registering test...")
        runner.register_test(
            name="debug_test", 
            description="Simple test to verify framework using natural language", 
            test_function=test_func
        )
        print("Test registered")
        
        print("Running tests...")
        results = await runner.run_tests()
        print(f"Got {len(results)} results")
        
        return True
    
    print("Running main...")
    result = asyncio.run(main())
    print(f"Result: {result}")
    
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
