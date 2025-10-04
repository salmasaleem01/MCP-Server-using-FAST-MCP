#!/usr/bin/env python3
"""
Test script for the Todo API
"""
import requests
import json
import time

BASE_URL = "http://localhost:8000"

def test_api():
    print("🧪 Testing Todo API...")
    
    # Test 1: Get welcome page
    try:
        response = requests.get(f"{BASE_URL}/")
        print(f"✅ Welcome page: {response.status_code}")
    except Exception as e:
        print(f"❌ Welcome page failed: {e}")
        return
    
    # Test 2: Get all todos (should be empty initially)
    try:
        response = requests.get(f"{BASE_URL}/todos")
        print(f"✅ Get todos: {response.status_code}")
        todos = response.json()
        print(f"   Found {len(todos)} todos")
    except Exception as e:
        print(f"❌ Get todos failed: {e}")
        return
    
    # Test 3: Create a new todo
    try:
        todo_data = {
            "title": "Learn FastAPI",
            "description": "Complete the FastAPI tutorial",
            "priority": 3,
            "status": "pending"
        }
        response = requests.post(f"{BASE_URL}/todos", json=todo_data)
        print(f"✅ Create todo: {response.status_code}")
        if response.status_code == 201:
            created_todo = response.json()
            todo_id = created_todo["todo"]["id"]
            print(f"   Created todo with ID: {todo_id}")
        else:
            print(f"   Response: {response.text}")
            return
    except Exception as e:
        print(f"❌ Create todo failed: {e}")
        return
    
    # Test 4: Get the created todo
    try:
        response = requests.get(f"{BASE_URL}/todos/{todo_id}")
        print(f"✅ Get specific todo: {response.status_code}")
        todo = response.json()
        print(f"   Todo title: {todo['title']}")
    except Exception as e:
        print(f"❌ Get specific todo failed: {e}")
    
    # Test 5: Update todo status
    try:
        response = requests.patch(f"{BASE_URL}/todos/{todo_id}/status", json={"status": "in_progress"})
        print(f"✅ Update status: {response.status_code}")
    except Exception as e:
        print(f"❌ Update status failed: {e}")
    
    # Test 6: Get statistics
    try:
        response = requests.get(f"{BASE_URL}/todos/stats/summary")
        print(f"✅ Get stats: {response.status_code}")
        stats = response.json()
        print(f"   Total todos: {stats['total_todos']}")
        print(f"   Completion rate: {stats['completion_rate']}%")
    except Exception as e:
        print(f"❌ Get stats failed: {e}")
    
    # Test 7: Search todos
    try:
        response = requests.get(f"{BASE_URL}/todos?search=FastAPI")
        print(f"✅ Search todos: {response.status_code}")
        search_results = response.json()
        print(f"   Found {len(search_results)} matching todos")
    except Exception as e:
        print(f"❌ Search todos failed: {e}")
    
    print("\n🎉 API testing completed!")

if __name__ == "__main__":
    print("Waiting for server to start...")
    time.sleep(3)
    test_api()

