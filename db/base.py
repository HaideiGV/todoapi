from bson import ObjectId
from pymongo import MongoClient

from settings import MONGODB_CONNECTION_URL


def get_db():
    connection = MongoClient(MONGODB_CONNECTION_URL)
    return connection["todo"]


def validate_id(_id):
    return ObjectId.is_valid(_id)


def convert_id(obj):
    if not obj:
        return

    obj["id"] = str(obj["_id"])
    del obj["_id"]

    return obj
