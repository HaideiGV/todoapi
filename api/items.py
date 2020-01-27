from fastapi import HTTPException, APIRouter
from starlette.status import (
    HTTP_200_OK,
    HTTP_404_NOT_FOUND,
    HTTP_400_BAD_REQUEST,
)

from db.items import add_todo_item, delete_item, update_item
from db.base import validate_id
from db.todos import get_todo_by_id
from db.models import ToDoItem, ToDoBaseItem

router = APIRouter()


@router.post(
    "/{todo_id}/items",
    response_model=ToDoItem,
    responses={
        HTTP_200_OK: {
            "description": "Ok",
            "content": {
                "application/json": {
                    "example": {
                        "id": "5e2c8a4cf9d7685d4b6e402d",
                        "todo_id": "5e2c8a4cf9d1115d4b6e402d",
                        "text": "Some Text",
                        "due_date": "2020-01-27T01:09:45.650Z",
                        "is_finished": "false",
                    }
                }
            },
        },
        HTTP_404_NOT_FOUND: {"description": "ToDo not found"},
    },
)
def create_todo_item(todo_id, item: ToDoBaseItem):
    is_valid_item_id = validate_id(todo_id)
    is_valid_id = validate_id(item.todo_id)
    if not is_valid_item_id or not is_valid_id:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="ToDo or ToDo id is not valid."
        )

    todo = get_todo_by_id(todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="ToDo not found")

    return add_todo_item(item)


@router.delete(
    "/{todo_id}/items/{item_id}",
    responses={
        HTTP_200_OK: {"description": "Ok"},
        HTTP_404_NOT_FOUND: {"description": "ToDoItem not found"},
    },
)
def delete_todo_item(todo_id: str, item_id: str):
    is_valid_item_id = validate_id(todo_id)
    is_valid_id = validate_id(item_id)
    if not is_valid_item_id or not is_valid_id:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="ToDo or ToDo id is not valid."
        )
    item = delete_item(item_id)
    if item.deleted_count:
        return HTTPException(status_code=200)
    raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="ToDoItem not found")


@router.put(
    "/{todo_id}/items/{item_id}",
    response_model=ToDoItem,
    responses={
        HTTP_200_OK: {
            "description": "Ok",
            "content": {
                "application/json": {
                    "example": {
                        "id": "5e2c8a4cf9d7685d4b6e402d",
                        "todo_id": "5e2c8a4cf9d1115d4b6e402d",
                        "text": "Some Text",
                        "due_date": "2020-01-27T01:09:45.650Z",
                        "is_finished": "false",
                    }
                }
            },
        },
        HTTP_404_NOT_FOUND: {"description": "ToDo not found"},
    },
)
def update_todo_item(todo_id: str, item_id: str, todo_item_data: ToDoItem):
    is_valid_item_id = validate_id(todo_id)
    is_valid_model_id = validate_id(todo_item_data.todo_id)
    is_valid_id = validate_id(todo_id)
    if not all([is_valid_item_id, is_valid_id, is_valid_model_id]):
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="ToDo or ToDo id is not valid."
        )

    item = update_item(item_id, todo_item_data)

    if not item:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="ToDoItem not found")

    return item
