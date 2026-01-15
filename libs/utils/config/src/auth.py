from libs.utils.config.src import config

SECRET_KEY = config.get("SECRET_KEY", "jamshi")
ACCESS_TOKEN_EXPIRE_MINUTES = int(config.get("ACCESS_TOKEN_EXPIRE_MINUTES", 30))
REFRESH_TOKEN_EXPIRE_DAYS = int(config.get("REFRESH_TOKEN_EXPIRE_DAYS", 30))
ALGORITHM = config.get("ALGORITHM", "HS256")
