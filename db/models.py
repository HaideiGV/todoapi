from datetime import datetime
from typing import List

from pydantic import BaseModel


class ToDoBaseItem(BaseModel):
    todo_id: str
    text: str
    due_date: datetime
    is_finished: bool = False


class ToDoItem(ToDoBaseItem):
    id: str = None


class ToDoBase(BaseModel):
    name: str


class ToDo(ToDoBase):
    id: str = None


class ToDoResponse(ToDo):
    items: List[ToDoItem]
