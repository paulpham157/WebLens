#!/usr/bin/env python3
"""
Very basic test
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
        return True
    
    async def main():
        print("Creating runner...")
        runner = TestRunner()
        print("Runner created")
        
        print("Registering test...")
        runner.register_test("test", "description", test_func)
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
