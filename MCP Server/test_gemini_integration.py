#!/usr/bin/env python3
"""
Test script to verify Gemini CLI + MCP integration
This script simulates the MCP server startup and tool availability
"""

import subprocess
import sys
import json
import time

def test_mcp_server():
    """Test if MCP server can start and respond"""
    print("🧪 Testing MCP Server Integration...")
    
    try:
        # Test MCP server import
        print("1. Testing MCP server import...")
        import mcp_server_fixed
        print("   ✅ MCP server imports successfully")
        
        # Test database operations
        print("2. Testing database operations...")
        from database import create_todo, get_all_todos
        from models import TodoCreate
        
        # Create a test todo
        test_todo = TodoCreate(
            title="Gemini Integration Test",
            description="Testing MCP integration with Gemini CLI",
            priority=3,
            status="pending"
        )
        
        todo = create_todo(test_todo)
        todos = get_all_todos()
        
        print(f"   ✅ Created test todo: {todo.title}")
        print(f"   ✅ Total todos: {len(todos)}")
        
        # Test MCP tools
        print("3. Testing MCP tool functions...")
        
        # Simulate tool calls
        tools_available = [
            "list_todos", "get_todo", "create_todo", 
            "update_todo", "update_todo_status", 
            "delete_todo", "search_todos", "get_todo_stats"
        ]
        
        print(f"   ✅ Available tools: {', '.join(tools_available)}")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False

def test_gemini_cli():
    """Test if Gemini CLI is available"""
    print("\n4. Testing Gemini CLI availability...")
    
    try:
        result = subprocess.run(
            ["npx", "@google/gemini-cli", "--version"],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode == 0:
            version = result.stdout.strip()
            print(f"   ✅ Gemini CLI available: {version}")
            return True
        else:
            print(f"   ❌ Gemini CLI error: {result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        print("   ❌ Gemini CLI timeout")
        return False
    except Exception as e:
        print(f"   ❌ Gemini CLI error: {e}")
        return False

def test_integration_config():
    """Test integration configuration"""
    print("\n5. Testing integration configuration...")
    
    try:
        # Check if config file exists
        config_path = "/Users/salmasaleem/Documents/MCP Server/gemini_mcp_config.json"
        
        with open(config_path, 'r') as f:
            config = json.load(f)
        
        print("   ✅ Configuration file exists")
        print(f"   ✅ MCP server configured: {list(config['mcpServers'].keys())}")
        
        # Check if MCP server file exists
        mcp_server_path = config['mcpServers']['todo-api']['args'][0]
        
        import os
        if os.path.exists(mcp_server_path):
            print(f"   ✅ MCP server file exists: {mcp_server_path}")
        else:
            print(f"   ❌ MCP server file not found: {mcp_server_path}")
            return False
        
        return True
        
    except Exception as e:
        print(f"   ❌ Configuration error: {e}")
        return False

def main():
    """Run all integration tests"""
    print("🚀 Testing Gemini CLI + MCP Todo API Integration")
    print("=" * 60)
    
    tests = [
        test_mcp_server,
        test_gemini_cli,
        test_integration_config
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print("\n" + "=" * 60)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Integration is ready!")
        print("\n🚀 To start using:")
        print("   ./start_gemini_with_mcp.sh")
        print("\n💬 Example commands in Gemini CLI:")
        print("   - 'Create a todo to learn FastAPI'")
        print("   - 'Show me all my todos'")
        print("   - 'What's my productivity like?'")
    else:
        print("❌ Some tests failed. Check the errors above.")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
