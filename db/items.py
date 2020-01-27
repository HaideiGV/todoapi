from bson import ObjectId
from pymongo import ReturnDocument

from db.models import ToDoBaseItem
from db.base import get_db, convert_id


def get_todo_item_by_id(_item_id):
    db = get_db()
    item = db.item.find_one({"_id": ObjectId(_item_id)})
    return convert_id(item)


def get_todo_item_by_todo_id(todo_id):
    db = get_db()
    items = db.item.find({"todo_id": todo_id})
    return [convert_id(item) for item in items]


def add_todo_item(item: ToDoBaseItem):
    db = get_db()
    data = db.item.insert_one(item.dict())
    return get_todo_item_by_id(data.inserted_id)


def delete_item(_item_id):
    db = get_db()
    return db.item.delete_one({"_id": ObjectId(_item_id)})


def update_item(_item_id, data):
    db = get_db()
    item = db.item.find_one_and_update(
        filter={"_id": ObjectId(_item_id)},
        update={"$set": data.dict()},
        return_document=ReturnDocument.AFTER,
    )
    return convert_id(item)
