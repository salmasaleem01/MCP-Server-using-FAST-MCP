from typing import List, Optional
from datetime import datetime
from models import Todo, TodoCreate, TodoUpdate, TodoStatus


# In-memory storage for demo purposes
# In a real application, you would use a proper database like PostgreSQL, SQLite, etc.
todos_db: List[Todo] = []
next_id = 1


def get_all_todos(status: Optional[TodoStatus] = None) -> List[Todo]:
    """Get all todos, optionally filtered by status"""
    if status:
        return [todo for todo in todos_db if todo.status == status]
    return todos_db.copy()


def get_todo_by_id(todo_id: int) -> Optional[Todo]:
    """Get a specific todo by ID"""
    for todo in todos_db:
        if todo.id == todo_id:
            return todo
    return None


def create_todo(todo_data: TodoCreate) -> Todo:
    """Create a new todo"""
    global next_id
    now = datetime.now()
    
    new_todo = Todo(
        id=next_id,
        title=todo_data.title,
        description=todo_data.description,
        status=todo_data.status,
        priority=todo_data.priority,
        created_at=now,
        updated_at=now
    )
    
    todos_db.append(new_todo)
    next_id += 1
    return new_todo


def update_todo(todo_id: int, todo_data: TodoUpdate) -> Optional[Todo]:
    """Update an existing todo"""
    for i, todo in enumerate(todos_db):
        if todo.id == todo_id:
            update_data = todo_data.dict(exclude_unset=True)
            now = datetime.now()
            
            updated_todo = Todo(
                id=todo.id,
                title=update_data.get('title', todo.title),
                description=update_data.get('description', todo.description),
                status=update_data.get('status', todo.status),
                priority=update_data.get('priority', todo.priority),
                created_at=todo.created_at,
                updated_at=now
            )
            
            todos_db[i] = updated_todo
            return updated_todo
    return None


def delete_todo(todo_id: int) -> bool:
    """Delete a todo by ID"""
    for i, todo in enumerate(todos_db):
        if todo.id == todo_id:
            del todos_db[i]
            return True
    return False


def search_todos(query: str) -> List[Todo]:
    """Search todos by title or description"""
    query_lower = query.lower()
    return [
        todo for todo in todos_db 
        if query_lower in todo.title.lower() or 
           (todo.description and query_lower in todo.description.lower())
    ]
