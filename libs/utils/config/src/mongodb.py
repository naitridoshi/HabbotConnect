from libs.utils.config.src import config

MONGO_URI = config.get("MONGO_URI", "mongodb://localhost:27017/")
MONGO_DATABASE_NAME = config.get("MONGO_DATABASE_NAME", "habbot_connect_db")
