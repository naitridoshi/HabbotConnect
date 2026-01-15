from libs.utils.config.src import config

SECRET_KEY = config.get("SECRET_KEY", "jamshi")
ACCESS_TOKEN_EXPIRE_MINUTES = int(config.get("ACCESS_TOKEN_EXPIRE_MINUTES", 30))
ALGORITHM = config.get("ALGORITHM", "HS256")

JAMSHI_SYSTEM_USER_FIRST_NAME = config.get("JAMSHI_SYSTEM_USER_FIRST_NAME")
JAMSHI_SYSTEM_USER_LAST_NAME = config.get("JAMSHI_SYSTEM_USER_LAST_NAME")
JAMSHI_SYSTEM_USER_EMAIL: str | None = config.get("JAMSHI_SYSTEM_USER_EMAIL")
JAMSHI_SYSTEM_USER_PASSWORD = config.get("JAMSHI_SYSTEM_USER_PASSWORD")

required = {
    "JAMSHI_SYSTEM_USER_EMAIL": JAMSHI_SYSTEM_USER_EMAIL,
    "JAMSHI_SYSTEM_USER_PASSWORD": JAMSHI_SYSTEM_USER_PASSWORD,
    "JAMSHI_SYSTEM_USER_FIRST_NAME": JAMSHI_SYSTEM_USER_FIRST_NAME,
    "JAMSHI_SYSTEM_USER_LAST_NAME": JAMSHI_SYSTEM_USER_LAST_NAME,
}
missing = [name for name, val in required.items() if not val]
if missing:
    raise ValueError(
        f"FastApi App is missing required config value(s): {', '.join(missing)}"
    )
