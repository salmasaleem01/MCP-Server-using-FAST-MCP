#!/bin/bash

# Start Gemini CLI with MCP Todo API integration
# This script sets up the environment and starts Gemini CLI with your Todo MCP server

echo "🚀 Starting Gemini CLI with Todo MCP Server..."
echo "📍 MCP Server: Todo API with FastAPI backend"
echo "🛠️  Available Tools: list_todos, create_todo, update_todo, delete_todo, search_todos, get_todo_stats"
echo ""

# Set environment variables
export PYTHONPATH="/Users/salmasaleem/Documents/MCP Server"

# Check if MCP server file exists
if [ ! -f "/Users/salmasaleem/Documents/MCP Server/mcp_server_fixed.py" ]; then
    echo "❌ Error: MCP server file not found!"
    echo "Please ensure mcp_server_fixed.py exists in the MCP Server directory"
    exit 1
fi

# Check if Python dependencies are installed
echo "🔍 Checking Python dependencies..."
python3 -c "import mcp" 2>/dev/null || {
    echo "❌ MCP dependencies not found. Installing..."
    pip3 install mcp
}

echo "✅ Dependencies ready"
echo ""

# Start Gemini CLI with MCP configuration
echo "🎯 Starting Gemini CLI..."
echo "💡 Once started, you can:"
echo "   - Use /mcp to see available MCP servers"
echo "   - Ask me to create, list, update, or delete todos"
echo "   - Request statistics about your todos"
echo ""

# Start Gemini CLI (default mode is interactive)
npx @google/gemini-cli
