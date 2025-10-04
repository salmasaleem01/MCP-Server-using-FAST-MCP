# Todo API with FastAPI

A simple and powerful Todo application built with FastAPI, featuring full CRUD operations, filtering, search, and automatic API documentation.

## Features

- ✅ **Full CRUD Operations**: Create, read, update, and delete todos
- 🔍 **Search & Filter**: Search todos by title/description and filter by status
- 📊 **Priority Levels**: Set priority from 1-5 for better organization
- 📈 **Statistics**: Get summary statistics about your todos
- 🎯 **Status Management**: Track todos as pending, in progress, or completed
- ⏰ **Automatic Timestamps**: Created and updated timestamps
- 📚 **Interactive Documentation**: Built-in Swagger UI and ReDoc
- ✅ **Input Validation**: Comprehensive validation with helpful error messages

## Installation

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the application**:
   ```bash
   python main.py
   ```
   
   Or using uvicorn directly:
   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

3. **Access the application**:
   - Main page: http://localhost:8000
   - Interactive API docs: http://localhost:8000/docs
   - ReDoc documentation: http://localhost:8000/redoc

## API Endpoints

### Basic Operations

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Welcome page with documentation links |
| GET | `/todos` | Get all todos (with optional filtering) |
| GET | `/todos/{id}` | Get a specific todo by ID |
| POST | `/todos` | Create a new todo |
| PUT | `/todos/{id}` | Update an existing todo |
| PATCH | `/todos/{id}/status` | Update only the status of a todo |
| DELETE | `/todos/{id}` | Delete a todo |
| GET | `/todos/stats/summary` | Get todo statistics |

### Query Parameters

- `status`: Filter todos by status (`pending`, `in_progress`, `completed`)
- `search`: Search todos by title or description

## Usage Examples

### Create a Todo
```bash
curl -X POST "http://localhost:8000/todos" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Learn FastAPI",
    "description": "Complete the FastAPI tutorial",
    "priority": 3,
    "status": "pending"
  }'
```

### Get All Todos
```bash
curl "http://localhost:8000/todos"
```

### Filter by Status
```bash
curl "http://localhost:8000/todos?status=completed"
```

### Search Todos
```bash
curl "http://localhost:8000/todos?search=FastAPI"
```

### Update a Todo
```bash
curl -X PUT "http://localhost:8000/todos/1" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Master FastAPI",
    "status": "in_progress"
  }'
```

### Update Todo Status Only
```bash
curl -X PATCH "http://localhost:8000/todos/1/status" \
  -H "Content-Type: application/json" \
  -d '{"status": "completed"}'
```

### Delete a Todo
```bash
curl -X DELETE "http://localhost:8000/todos/1"
```

### Get Statistics
```bash
curl "http://localhost:8000/todos/stats/summary"
```

## Data Models

### Todo Status
- `pending`: Todo is not started
- `in_progress`: Todo is being worked on
- `completed`: Todo is finished

### Priority Levels
- `1`: Lowest priority
- `5`: Highest priority

### Todo Fields
- `id`: Unique identifier (auto-generated)
- `title`: Todo title (required, 1-200 characters)
- `description`: Optional description (max 1000 characters)
- `status`: Current status (default: pending)
- `priority`: Priority level 1-5 (default: 1)
- `created_at`: Creation timestamp (auto-generated)
- `updated_at`: Last update timestamp (auto-generated)

## Development

The application uses in-memory storage for simplicity. In a production environment, you would typically use a database like PostgreSQL, SQLite, or MongoDB.

### Project Structure
```
├── main.py          # FastAPI application and routes
├── models.py        # Pydantic models for data validation
├── database.py      # In-memory database operations
├── requirements.txt # Python dependencies
└── README.md        # This file
```

## Error Handling

The API includes comprehensive error handling:
- **404**: Resource not found
- **422**: Validation errors
- **400**: Bad request (missing required fields)

All errors return JSON responses with descriptive messages.

## Interactive Documentation

FastAPI automatically generates interactive API documentation:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

You can test all endpoints directly from the documentation interface!

