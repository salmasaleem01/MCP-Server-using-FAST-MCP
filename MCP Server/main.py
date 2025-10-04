from fastapi import FastAPI, HTTPException, Query, Path
from fastapi.responses import HTMLResponse
from typing import List, Optional
from models import Todo, TodoCreate, TodoUpdate, TodoResponse, ErrorResponse, TodoStatus, StatusUpdate
from database import (
    get_all_todos, get_todo_by_id, create_todo, 
    update_todo, delete_todo, search_todos
)

# Create FastAPI app
app = FastAPI(
    title="Todo API",
    description="A simple Todo application built with FastAPI",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)


@app.get("/", response_class=HTMLResponse)
async def root():
    """Welcome page with API documentation link"""
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Todo API</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; background-color: #f5f5f5; }
            .container { max-width: 800px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
            h1 { color: #333; text-align: center; }
            .links { text-align: center; margin: 30px 0; }
            .links a { display: inline-block; margin: 10px; padding: 10px 20px; background: #007bff; color: white; text-decoration: none; border-radius: 5px; }
            .links a:hover { background: #0056b3; }
            .features { margin: 30px 0; }
            .features h3 { color: #555; }
            .features ul { color: #666; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🚀 Todo API</h1>
            <p style="text-align: center; color: #666; font-size: 18px;">
                A powerful and simple Todo application built with FastAPI
            </p>
            
            <div class="links">
                <a href="/docs">📚 Interactive API Docs</a>
                <a href="/redoc">📖 ReDoc Documentation</a>
            </div>
            
            <div class="features">
                <h3>✨ Features</h3>
                <ul>
                    <li>Create, read, update, and delete todos</li>
                    <li>Filter todos by status (pending, in_progress, completed)</li>
                    <li>Search todos by title or description</li>
                    <li>Priority levels (1-5)</li>
                    <li>Automatic timestamps</li>
                    <li>Input validation and error handling</li>
                </ul>
            </div>
        </div>
    </body>
    </html>
    """


@app.get("/todos", response_model=List[Todo])
async def get_todos(
    status: Optional[TodoStatus] = Query(None, description="Filter by todo status"),
    search: Optional[str] = Query(None, description="Search in title and description")
):
    """Get all todos with optional filtering and search"""
    if search:
        todos = search_todos(search)
        if status:
            todos = [todo for todo in todos if todo.status == status]
    else:
        todos = get_all_todos(status)
    
    return todos


@app.get("/todos/{todo_id}", response_model=Todo)
async def get_todo(todo_id: int = Path(..., description="Todo ID")):
    """Get a specific todo by ID"""
    todo = get_todo_by_id(todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo


@app.post("/todos", response_model=TodoResponse, status_code=201)
async def create_new_todo(todo_data: TodoCreate):
    """Create a new todo"""
    todo = create_todo(todo_data)
    return TodoResponse(message="Todo created successfully", todo=todo)


@app.put("/todos/{todo_id}", response_model=TodoResponse)
async def update_existing_todo(
    todo_id: int = Path(..., description="Todo ID"),
    todo_data: TodoUpdate = None
):
    """Update an existing todo"""
    if not todo_data:
        raise HTTPException(status_code=400, detail="Update data is required")
    
    todo = update_todo(todo_id, todo_data)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    
    return TodoResponse(message="Todo updated successfully", todo=todo)


@app.patch("/todos/{todo_id}/status", response_model=TodoResponse)
async def update_todo_status(
    status_data: StatusUpdate,
    todo_id: int = Path(..., description="Todo ID")
):
    """Update only the status of a todo"""
    todo_data = TodoUpdate(status=status_data.status)
    todo = update_todo(todo_id, todo_data)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    
    return TodoResponse(message="Todo status updated successfully", todo=todo)


@app.delete("/todos/{todo_id}", response_model=dict)
async def delete_existing_todo(todo_id: int = Path(..., description="Todo ID")):
    """Delete a todo"""
    if not delete_todo(todo_id):
        raise HTTPException(status_code=404, detail="Todo not found")
    
    return {"message": "Todo deleted successfully"}


@app.get("/todos/stats/summary", response_model=dict)
async def get_todo_stats():
    """Get statistics about todos"""
    all_todos = get_all_todos()
    total = len(all_todos)
    pending = len([t for t in all_todos if t.status == TodoStatus.PENDING])
    in_progress = len([t for t in all_todos if t.status == TodoStatus.IN_PROGRESS])
    completed = len([t for t in all_todos if t.status == TodoStatus.COMPLETED])
    
    return {
        "total_todos": total,
        "pending": pending,
        "in_progress": in_progress,
        "completed": completed,
        "completion_rate": round((completed / total * 100) if total > 0 else 0, 2)
    }


# Error handlers
@app.exception_handler(404)
async def not_found_handler(request, exc):
    return {"detail": "Resource not found"}


@app.exception_handler(422)
async def validation_error_handler(request, exc):
    return {"detail": "Validation error", "errors": exc.errors()}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

