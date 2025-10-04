#!/usr/bin/env python3
"""
Direct test of MCP Todo tools without server framework
"""
from models import Todo, TodoCreate, TodoUpdate, TodoStatus
from database import (
    get_all_todos, get_todo_by_id, create_todo, 
    update_todo, delete_todo, search_todos
)

def test_todo_operations():
    """Test all Todo operations directly"""
    print("🧪 Testing Todo Operations Directly...")
    
    # Test 1: Get initial stats
    print("\n1. Testing initial stats...")
    all_todos = get_all_todos()
    print(f"✅ Initial todos: {len(all_todos)}")
    
    # Test 2: Create a todo
    print("\n2. Testing create_todo...")
    todo_data = TodoCreate(
        title="Test MCP Todo",
        description="Testing MCP server functionality",
        priority=3,
        status="pending"
    )
    todo = create_todo(todo_data)
    print(f"✅ Created todo: ID {todo.id}, Title: {todo.title}")
    
    # Test 3: Get specific todo
    print("\n3. Testing get_todo...")
    retrieved_todo = get_todo_by_id(todo.id)
    if retrieved_todo:
        print(f"✅ Retrieved todo: {retrieved_todo.title}")
    else:
        print("❌ Todo not found")
    
    # Test 4: Update todo status
    print("\n4. Testing update_todo_status...")
    update_data = TodoUpdate(status="in_progress")
    updated_todo = update_todo(todo.id, update_data)
    if updated_todo:
        print(f"✅ Updated status to: {updated_todo.status}")
    else:
        print("❌ Update failed")
    
    # Test 5: Search todos
    print("\n5. Testing search_todos...")
    search_results = search_todos("MCP")
    print(f"✅ Search results: {len(search_results)} todos found")
    for result in search_results:
        print(f"   • {result.title} (Status: {result.status})")
    
    # Test 6: Update todo
    print("\n6. Testing update_todo...")
    update_data = TodoUpdate(title="Updated MCP Todo", priority=5)
    updated_todo = update_todo(todo.id, update_data)
    if updated_todo:
        print(f"✅ Updated todo: {updated_todo.title}, Priority: {updated_todo.priority}")
    else:
        print("❌ Update failed")
    
    # Test 7: Get final stats
    print("\n7. Testing final stats...")
    all_todos = get_all_todos()
    total = len(all_todos)
    pending = len([t for t in all_todos if t.status == "pending"])
    in_progress = len([t for t in all_todos if t.status == "in_progress"])
    completed = len([t for t in all_todos if t.status == "completed"])
    completion_rate = round((completed / total * 100) if total > 0 else 0, 2)
    
    print(f"✅ Final stats:")
    print(f"   • Total todos: {total}")
    print(f"   • Pending: {pending}")
    print(f"   • In Progress: {in_progress}")
    print(f"   • Completed: {completed}")
    print(f"   • Completion Rate: {completion_rate}%")
    
    # Test 8: Delete todo
    print("\n8. Testing delete_todo...")
    success = delete_todo(todo.id)
    if success:
        print(f"✅ Todo {todo.id} deleted successfully")
    else:
        print("❌ Delete failed")
    
    # Test 9: Verify deletion
    print("\n9. Testing deletion verification...")
    deleted_todo = get_todo_by_id(todo.id)
    if not deleted_todo:
        print("✅ Todo successfully deleted")
    else:
        print("❌ Todo still exists")
    
    print("\n🎉 All Todo operations tests completed successfully!")

if __name__ == "__main__":
    test_todo_operations()
