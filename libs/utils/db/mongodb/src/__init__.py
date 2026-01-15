from pymongo import MongoClient
from pymongo.errors import PyMongoError

from libs.utils.config.src.mongodb import MONGO_DATABASE_NAME, MONGO_URI


def connect_db(db_name: str):
    try:
        client = MongoClient(MONGO_URI)
        return client[db_name]
    except PyMongoError as error:
        raise Exception(
            f'Failed to connect to database: "{db_name}",ERROR: {str(error)}'
        )


db = connect_db(MONGO_DATABASE_NAME)
