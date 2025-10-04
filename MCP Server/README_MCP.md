# Todo API MCP Server

This MCP (Model Context Protocol) server provides tools to interact with your FastAPI Todo application through MCP-compatible clients.

## Features

The MCP server exposes the following tools:

### 📋 Todo Management Tools
- **`list_todos`** - Get all todos with optional filtering by status and search
- **`get_todo`** - Get a specific todo by ID
- **`create_todo`** - Create a new todo
- **`update_todo`** - Update an existing todo
- **`update_todo_status`** - Update only the status of a todo
- **`delete_todo`** - Delete a todo by ID

### 🔍 Search & Analytics Tools
- **`search_todos`** - Search todos by title or description
- **`get_todo_stats`** - Get statistics about todos

## Installation

1. **Install MCP dependencies**:
   ```bash
   pip3 install -r requirements.txt
   ```

2. **Make the MCP server executable**:
   ```bash
   chmod +x mcp_server.py
   chmod +x start_mcp_server.py
   ```

## Usage

### Starting the MCP Server

```bash
python3 start_mcp_server.py
```

### Configuration

The MCP server can be configured using the `mcp_config.json` file:

```json
{
  "mcpServers": {
    "todo-api": {
      "command": "python3",
      "args": ["/path/to/your/mcp_server.py"],
      "env": {
        "PYTHONPATH": "/path/to/your/project"
      }
    }
  }
}
```

## Tool Descriptions

### list_todos
Get all todos with optional filtering.

**Parameters:**
- `status` (optional): Filter by status ("pending", "in_progress", "completed")
- `search` (optional): Search in title and description

**Example:**
```json
{
  "status": "pending",
  "search": "important"
}
```

### get_todo
Get a specific todo by ID.

**Parameters:**
- `todo_id` (required): The ID of the todo to retrieve

### create_todo
Create a new todo.

**Parameters:**
- `title` (required): Todo title (1-200 characters)
- `description` (optional): Todo description (max 1000 characters)
- `priority` (optional): Priority level 1-5 (default: 1)
- `status` (optional): Todo status (default: "pending")

### update_todo
Update an existing todo.

**Parameters:**
- `todo_id` (required): The ID of the todo to update
- `title` (optional): New title
- `description` (optional): New description
- `priority` (optional): New priority level
- `status` (optional): New status

### update_todo_status
Update only the status of a todo.

**Parameters:**
- `todo_id` (required): The ID of the todo to update
- `status` (required): New status ("pending", "in_progress", "completed")

### delete_todo
Delete a todo by ID.

**Parameters:**
- `todo_id` (required): The ID of the todo to delete

### search_todos
Search todos by title or description.

**Parameters:**
- `query` (required): Search query

### get_todo_stats
Get statistics about todos.

**Returns:**
- Total todos count
- Count by status (pending, in_progress, completed)
- Completion rate percentage

## Testing

Run the test script to verify all tools work correctly:

```bash
python3 test_mcp_tools.py
```

## Integration with MCP Clients

This MCP server can be used with any MCP-compatible client, such as:

- **Claude Desktop** - Add the server to your Claude Desktop configuration
- **Custom MCP clients** - Use the standard MCP protocol
- **AI assistants** - Integrate with AI systems that support MCP

## Error Handling

The MCP server includes comprehensive error handling:

- **Validation errors** - Invalid input parameters
- **Not found errors** - Todo ID doesn't exist
- **Server errors** - Database or system errors

All errors are returned as text content with descriptive messages.

## Development

The MCP server is built using the official MCP Python SDK and integrates directly with your FastAPI Todo application's database layer.

### Project Structure
```
├── mcp_server.py          # Main MCP server implementation
├── start_mcp_server.py    # Server startup script
├── test_mcp_tools.py      # Test script for all tools
├── mcp_config.json        # MCP server configuration
└── README_MCP.md          # This documentation
```

## Troubleshooting

1. **Import errors**: Ensure all dependencies are installed and PYTHONPATH is set correctly
2. **Tool not found**: Check that the MCP server is running and properly configured
3. **Database errors**: Ensure the FastAPI Todo application database is accessible

For more information about MCP, visit the [Model Context Protocol documentation](https://modelcontextprotocol.io/).
