from typing import List

from fastapi import HTTPException, APIRouter
from starlette.status import (
    HTTP_200_OK,
    HTTP_404_NOT_FOUND,
    HTTP_400_BAD_REQUEST,
)

from db.items import get_todo_item_by_todo_id
from db.todos import (
    get_todo_by_id,
    add_todo,
    change_todo,
    get_todo_list,
    remove_todo,
)
from db.base import validate_id
from db.models import ToDo, ToDoBase, ToDoResponse

router = APIRouter()


@router.get(
    "/",
    response_model=List[ToDoResponse],
    responses={
        HTTP_200_OK: {
            "description": "Ok",
            "content": {
                "application/json": {
                    "example": [{"id": "5e2c8a4cf9d7685d4b6e402d", "name": "SomeName"}]
                }
            },
        },
        HTTP_404_NOT_FOUND: {"description": "ToDo not found"},
    },
)
def get_todos():
    data = get_todo_list()
    if not data:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND)
    for todo in data:
        todo.update({"items": get_todo_item_by_todo_id(todo["id"])})
    return data


@router.get(
    "/{todo_id}",
    response_model=ToDoResponse,
    responses={
        HTTP_200_OK: {
            "description": "Ok",
            "content": {
                "application/json": {
                    "example": {
                        "id": "5e2c8a4cf9d7685d4b6e402d",
                        "name": "SomeName",
                        "items": [
                            {
                                "id": "5e2c8a4cf9d7685d4b6e402d",
                                "todo_id": "5e2c8a4cf9d1115d4b6e402d",
                                "text": "Some Text",
                                "due_date": "2020-01-27T01:09:45.650Z",
                                "is_finished": "false",
                            }
                        ],
                    }
                }
            },
        },
        HTTP_404_NOT_FOUND: {"description": "ToDo not found"},
    },
)
def get_todo(todo_id: str):
    is_valid_id = validate_id(todo_id)
    if not is_valid_id:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="ToDo id is not valid."
        )

    todo = get_todo_by_id(todo_id)
    if not todo:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="ToDo not found")
    todo["items"] = get_todo_item_by_todo_id(todo_id)
    return todo


@router.delete(
    "/{todo_id}",
    status_code=HTTP_200_OK,
    responses={
        HTTP_200_OK: {"description": "Ok"},
        HTTP_404_NOT_FOUND: {"description": "ToDo not found"},
    },
)
def delete_todo(todo_id: str):
    is_valid_id = validate_id(todo_id)
    if not is_valid_id:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="ToDo id is not valid."
        )
    todo = remove_todo(todo_id)
    if todo.deleted_count:
        return HTTPException(status_code=200)
    raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="ToDo not found")


@router.post(
    "/",
    status_code=HTTP_200_OK,
    responses={
        HTTP_200_OK: {
            "description": "Ok",
            "content": {"application/json": {"example": {"name": "SomeName"}}},
        }
    },
)
def create_todo(todo: ToDoBase):
    return add_todo(todo)


@router.put(
    "/{todo_id}",
    response_model=ToDo,
    status_code=HTTP_200_OK,
    responses={
        HTTP_200_OK: {
            "description": "Ok",
            "content": {"application/json": {"example": {"name": "SomeName"}}},
        }
    },
)
def update_todo(todo_id: str, todo_data: ToDoBase):
    is_valid_id = validate_id(todo_id)
    if not is_valid_id:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="ToDo id is not valid."
        )

    todo = change_todo(todo_id, todo_data)

    if not todo:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="ToDo not found")

    return todo
