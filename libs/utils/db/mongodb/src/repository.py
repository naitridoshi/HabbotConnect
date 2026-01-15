from libs.utils.db.mongodb.src import db
from libs.utils.db.mongodb.src.base_repository import BaseRepository

# Collection references
users_collection = db["users"]


# Repository instances
users_repository = BaseRepository(collection=users_collection, timestamps=True)


__all__ = [
    "users_repository",
]
