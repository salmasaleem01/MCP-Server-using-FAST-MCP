#!/usr/bin/env python3
"""
MCP Server for Todo API
Provides tools to interact with the FastAPI Todo application
"""

import asyncio
import json
from typing import Any, Dict, List, Optional
from datetime import datetime

# MCP imports
from mcp.server import Server
from mcp.server.models import InitializationOptions
from mcp.server.stdio import stdio_server
from mcp.types import (
    CallToolRequest,
    CallToolResult,
    ListToolsRequest,
    ListToolsResult,
    Tool,
    TextContent,
    ImageContent,
    EmbeddedResource,
)

# Import our Todo API components
from models import Todo, TodoCreate, TodoUpdate, TodoStatus
from database import (
    get_all_todos, get_todo_by_id, create_todo, 
    update_todo, delete_todo, search_todos
)

# Create MCP server instance
server = Server("todo-api-mcp")

@server.list_tools()
async def handle_list_tools() -> ListToolsResult:
    """List all available MCP tools for Todo operations"""
    return ListToolsResult(
        tools=[
            Tool(
                name="list_todos",
                description="Get all todos with optional filtering by status",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "status": {
                            "type": "string",
                            "enum": ["pending", "in_progress", "completed"],
                            "description": "Filter todos by status (optional)"
                        },
                        "search": {
                            "type": "string",
                            "description": "Search todos by title or description (optional)"
                        }
                    }
                }
            ),
            Tool(
                name="get_todo",
                description="Get a specific todo by ID",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "todo_id": {
                            "type": "integer",
                            "description": "The ID of the todo to retrieve"
                        }
                    },
                    "required": ["todo_id"]
                }
            ),
            Tool(
                name="create_todo",
                description="Create a new todo",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "title": {
                            "type": "string",
                            "description": "Todo title (required, 1-200 characters)"
                        },
                        "description": {
                            "type": "string",
                            "description": "Todo description (optional, max 1000 characters)"
                        },
                        "priority": {
                            "type": "integer",
                            "minimum": 1,
                            "maximum": 5,
                            "description": "Priority level 1-5 (optional, default: 1)"
                        },
                        "status": {
                            "type": "string",
                            "enum": ["pending", "in_progress", "completed"],
                            "description": "Todo status (optional, default: pending)"
                        }
                    },
                    "required": ["title"]
                }
            ),
            Tool(
                name="update_todo",
                description="Update an existing todo",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "todo_id": {
                            "type": "integer",
                            "description": "The ID of the todo to update"
                        },
                        "title": {
                            "type": "string",
                            "description": "New title (optional)"
                        },
                        "description": {
                            "type": "string",
                            "description": "New description (optional)"
                        },
                        "priority": {
                            "type": "integer",
                            "minimum": 1,
                            "maximum": 5,
                            "description": "New priority level (optional)"
                        },
                        "status": {
                            "type": "string",
                            "enum": ["pending", "in_progress", "completed"],
                            "description": "New status (optional)"
                        }
                    },
                    "required": ["todo_id"]
                }
            ),
            Tool(
                name="update_todo_status",
                description="Update only the status of a todo",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "todo_id": {
                            "type": "integer",
                            "description": "The ID of the todo to update"
                        },
                        "status": {
                            "type": "string",
                            "enum": ["pending", "in_progress", "completed"],
                            "description": "New status"
                        }
                    },
                    "required": ["todo_id", "status"]
                }
            ),
            Tool(
                name="delete_todo",
                description="Delete a todo by ID",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "todo_id": {
                            "type": "integer",
                            "description": "The ID of the todo to delete"
                        }
                    },
                    "required": ["todo_id"]
                }
            ),
            Tool(
                name="search_todos",
                description="Search todos by title or description",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "Search query"
                        }
                    },
                    "required": ["query"]
                }
            ),
            Tool(
                name="get_todo_stats",
                description="Get statistics about todos",
                inputSchema={
                    "type": "object",
                    "properties": {}
                }
            )
        ]
    )

@server.call_tool()
async def handle_call_tool(name: str, arguments: Dict[str, Any]) -> CallToolResult:
    """Handle tool calls for Todo operations"""
    
    try:
        if name == "list_todos":
            status = arguments.get("status")
            search = arguments.get("search")
            
            if search:
                todos = search_todos(search)
                if status:
                    todos = [todo for todo in todos if todo.status == status]
            else:
                todos = get_all_todos(status)
            
            result = {
                "todos": [
                    {
                        "id": todo.id,
                        "title": todo.title,
                        "description": todo.description,
                        "status": todo.status,
                        "priority": todo.priority,
                        "created_at": todo.created_at.isoformat(),
                        "updated_at": todo.updated_at.isoformat()
                    }
                    for todo in todos
                ],
                "count": len(todos)
            }
            
            return CallToolResult(
                content=[TextContent(
                    type="text",
                    text=f"Found {len(todos)} todos:\n\n" + 
                         "\n".join([
                             f"• {todo.title} (ID: {todo.id}, Status: {todo.status}, Priority: {todo.priority})"
                             for todo in todos
                         ])
                )]
            )
        
        elif name == "get_todo":
            todo_id = arguments["todo_id"]
            todo = get_todo_by_id(todo_id)
            
            if not todo:
                return CallToolResult(
                    content=[TextContent(
                        type="text",
                        text=f"Todo with ID {todo_id} not found"
                    )]
                )
            
            return CallToolResult(
                content=[TextContent(
                    type="text",
                    text=f"Todo Details:\n"
                         f"• ID: {todo.id}\n"
                         f"• Title: {todo.title}\n"
                         f"• Description: {todo.description or 'No description'}\n"
                         f"• Status: {todo.status}\n"
                         f"• Priority: {todo.priority}\n"
                         f"• Created: {todo.created_at.strftime('%Y-%m-%d %H:%M:%S')}\n"
                         f"• Updated: {todo.updated_at.strftime('%Y-%m-%d %H:%M:%S')}"
                )]
            )
        
        elif name == "create_todo":
            todo_data = TodoCreate(
                title=arguments["title"],
                description=arguments.get("description"),
                priority=arguments.get("priority", 1),
                status=arguments.get("status", "pending")
            )
            
            todo = create_todo(todo_data)
            
            return CallToolResult(
                content=[TextContent(
                    type="text",
                    text=f"✅ Todo created successfully!\n"
                         f"• ID: {todo.id}\n"
                         f"• Title: {todo.title}\n"
                         f"• Status: {todo.status}\n"
                         f"• Priority: {todo.priority}"
                )]
            )
        
        elif name == "update_todo":
            todo_id = arguments["todo_id"]
            update_data = TodoUpdate(
                title=arguments.get("title"),
                description=arguments.get("description"),
                priority=arguments.get("priority"),
                status=arguments.get("status")
            )
            
            todo = update_todo(todo_id, update_data)
            
            if not todo:
                return CallToolResult(
                    content=[TextContent(
                        type="text",
                        text=f"Todo with ID {todo_id} not found"
                    )]
                )
            
            return CallToolResult(
                content=[TextContent(
                    type="text",
                    text=f"✅ Todo updated successfully!\n"
                         f"• ID: {todo.id}\n"
                         f"• Title: {todo.title}\n"
                         f"• Status: {todo.status}\n"
                         f"• Priority: {todo.priority}"
                )]
            )
        
        elif name == "update_todo_status":
            todo_id = arguments["todo_id"]
            status = arguments["status"]
            
            update_data = TodoUpdate(status=status)
            todo = update_todo(todo_id, update_data)
            
            if not todo:
                return CallToolResult(
                    content=[TextContent(
                        type="text",
                        text=f"Todo with ID {todo_id} not found"
                    )]
                )
            
            return CallToolResult(
                content=[TextContent(
                    type="text",
                    text=f"✅ Todo status updated to '{status}'!\n"
                         f"• ID: {todo.id}\n"
                         f"• Title: {todo.title}\n"
                         f"• New Status: {todo.status}"
                )]
            )
        
        elif name == "delete_todo":
            todo_id = arguments["todo_id"]
            success = delete_todo(todo_id)
            
            if not success:
                return CallToolResult(
                    content=[TextContent(
                        type="text",
                        text=f"Todo with ID {todo_id} not found"
                    )]
                )
            
            return CallToolResult(
                content=[TextContent(
                    type="text",
                    text=f"✅ Todo with ID {todo_id} deleted successfully"
                )]
            )
        
        elif name == "search_todos":
            query = arguments["query"]
            todos = search_todos(query)
            
            return CallToolResult(
                content=[TextContent(
                    type="text",
                    text=f"Search results for '{query}' ({len(todos)} found):\n\n" +
                         "\n".join([
                             f"• {todo.title} (ID: {todo.id}, Status: {todo.status})"
                             for todo in todos
                         ]) if todos else f"No todos found matching '{query}'"
                )]
            )
        
        elif name == "get_todo_stats":
            all_todos = get_all_todos()
            total = len(all_todos)
            pending = len([t for t in all_todos if t.status == "pending"])
            in_progress = len([t for t in all_todos if t.status == "in_progress"])
            completed = len([t for t in all_todos if t.status == "completed"])
            completion_rate = round((completed / total * 100) if total > 0 else 0, 2)
            
            return CallToolResult(
                content=[TextContent(
                    type="text",
                    text=f"📊 Todo Statistics:\n"
                         f"• Total todos: {total}\n"
                         f"• Pending: {pending}\n"
                         f"• In Progress: {in_progress}\n"
                         f"• Completed: {completed}\n"
                         f"• Completion Rate: {completion_rate}%"
                )]
            )
        
        else:
            return CallToolResult(
                content=[TextContent(
                    type="text",
                    text=f"Unknown tool: {name}"
                )]
            )
    
    except Exception as e:
        return CallToolResult(
            content=[TextContent(
                type="text",
                text=f"Error executing tool '{name}': {str(e)}"
            )]
        )

async def main():
    """Main function to run the MCP server"""
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="todo-api-mcp",
                server_version="1.0.0",
                capabilities=server.get_capabilities(
                    notification_options=None,
                    experimental_capabilities=None,
                ),
            ),
        )

if __name__ == "__main__":
    asyncio.run(main())
