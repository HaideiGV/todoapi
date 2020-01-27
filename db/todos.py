from bson import ObjectId
from pymongo import ReturnDocument

from db.models import ToDoBase
from db.base import get_db, convert_id


def get_todo_list():
    db = get_db()
    return [convert_id(todo) for todo in db.todo.find()]


def get_todo_by_id(_id):
    db = get_db()
    todo = db.todo.find_one({"_id": ObjectId(_id)})
    return convert_id(todo)


def add_todo(todo: ToDoBase):
    db = get_db()
    created_todo = db.todo.insert_one(todo.dict())
    return get_todo_by_id(created_todo.inserted_id)


def remove_todo(_id):
    db = get_db()
    return db.todo.delete_one({"_id": ObjectId(_id)})


def change_todo(_id, data: ToDoBase):
    db = get_db()
    todo = db.todo.find_one_and_update(
        filter={"_id": ObjectId(_id)},
        update={"$set": data.dict()},
        return_document=ReturnDocument.AFTER,
    )
    return convert_id(todo)
