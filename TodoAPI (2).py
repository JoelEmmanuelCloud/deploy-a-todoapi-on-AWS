from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Any

app: Any = FastAPI(title="Todo API")

# Sample todo list
todos: list[dict] = [
    {"id": 1, "title": "Buy groceries", "completed": False},
    {"id": 2, "title": "Do laundry", "completed": True},
]

# Todo model
class Todo(BaseModel):
    title: str
    completed: bool = False

# Get all todos
@app.get('/todos', response_model=list[Todo])
def get_todos() -> list[dict]:
    return todos

# Get a todo by ID
@app.get('/todos/{todo_id}', response_model=Todo)
def get_todo_by_id(todo_id: int) -> Optional[dict]:
    todo = next((todo for todo in todos if todo["id"] == todo_id), None)
    if todo:
        return todo
    else:
        raise HTTPException(status_code=404, detail="Todo not found")

# Create a new todo
@app.post('/todos', response_model=Todo, status_code=201)
def create_todo(todo: Todo) -> dict:
    new_todo = {
        "id": len(todos) + 1,
        "title": todo.title,
        "completed": todo.completed
    }
    todos.append(new_todo)
    return new_todo

# Update a todo by ID
@app.put('/todos/{todo_id}', response_model=Todo)
def update_todo_by_id(todo_id: int, todo: Todo) -> Optional[dict]:
    index = next((index for index, todo in enumerate(todos) if todo["id"] == todo_id), None)
    if index is None:
        raise HTTPException(status_code=404, detail="Todo not found")

    todos[index]["title"] = todo.title
    todos[index]["completed"] = todo.completed

    return todos[index]

# Delete a todo by ID
@app.delete('/todos/{todo_id}', status_code=204)
def delete_todo_by_id(todo_id: int) -> None:
    global todos
    todos = [todo for todo in todos if todo["id"] != todo_id]


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=5000)