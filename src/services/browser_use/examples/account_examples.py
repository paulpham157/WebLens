"""
Account Management Examples for Browser Use API

This module provides examples of using the Account Management functionality.
"""
from ..controllers.account_manager import AccountManager

def check_account_balance():
    """Example showing how to check account balance"""
    account_manager = AccountManager()
    
    try:
        # Get account balance
        balance_info = account_manager.get_account_balance()
        
        print("📊 Account Balance Information:")
        print(f"  Credits remaining: {balance_info.get('credits_remaining', 'N/A')}")
        print(f"  Credits used: {balance_info.get('credits_used', 'N/A')}")
        print(f"  Total credits: {balance_info.get('total_credits', 'N/A')}")
        
        # Get more detailed usage info if available
        usage = balance_info.get('usage_details', {})
        if usage:
            print("\n📈 Usage Details:")
            print(f"  Tasks completed: {usage.get('tasks_completed', 'N/A')}")
            print(f"  Tasks failed: {usage.get('tasks_failed', 'N/A')}")
        
        return balance_info
    
    except Exception as e:
        print(f"❌ Error checking account balance: {e}")
        print("💡 Note: This feature may not be available in your current API version.")
        return None

def get_account_details():
    """Example showing how to get detailed account information"""
    account_manager = AccountManager()
    
    try:
        # Get account info
        account_info = account_manager.get_account_info()
        
        print("👤 Account Information:")
        print(f"  Account ID: {account_info.get('account_id', 'N/A')}")
        print(f"  Plan: {account_info.get('plan', 'N/A')}")
        print(f"  Status: {account_info.get('status', 'N/A')}")
        
        # Show limits if available
        limits = account_info.get('limits', {})
        if limits:
            print("\n⚙️ Account Limits:")
            for limit_name, limit_value in limits.items():
                print(f"  {limit_name}: {limit_value}")
        
        return account_info
    
    except Exception as e:
        print(f"❌ Error getting account details: {e}")
        print("💡 Note: This feature may not be available in your current API version.")
        return None

def get_usage_history(days: int = 30):
    """Example showing how to get usage history"""
    account_manager = AccountManager()
    
    try:
        # Get usage history
        history = account_manager.get_usage_history(days)
        
        print(f"📈 Usage History (Last {days} days):")
        
        daily_usage = history.get('daily_usage', [])
        if daily_usage:
            for day_data in daily_usage:
                date = day_data.get('date', 'Unknown')
                credits = day_data.get('credits_used', 0)
                tasks = day_data.get('tasks_completed', 0)
                print(f"  {date}: {credits} credits used, {tasks} tasks completed")
        else:
            print("  No usage history data available")
        
        return history
    
    except Exception as e:
        print(f"❌ Error getting usage history: {e}")
        print("💡 Note: This feature may not be available in your current API version.")
        return None
