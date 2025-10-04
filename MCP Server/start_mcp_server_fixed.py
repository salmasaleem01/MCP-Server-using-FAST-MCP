#!/usr/bin/env python3
"""
Start the MCP Server for Todo API - Fixed Version
"""
import asyncio
import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mcp_server_fixed import main

if __name__ == "__main__":
    print("🚀 Starting Todo API MCP Server (Fixed Version)...")
    print("📋 Available tools:")
    print("  • list_todos - Get all todos with optional filtering")
    print("  • get_todo - Get a specific todo by ID")
    print("  • create_todo - Create a new todo")
    print("  • update_todo - Update an existing todo")
    print("  • update_todo_status - Update only the status of a todo")
    print("  • delete_todo - Delete a todo by ID")
    print("  • search_todos - Search todos by title or description")
    print("  • get_todo_stats - Get statistics about todos")
    print("🛑 Press Ctrl+C to stop the server")
    print("-" * 50)
    
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 MCP Server stopped")
    except Exception as e:
        print(f"❌ Error starting MCP server: {e}")
        sys.exit(1)
