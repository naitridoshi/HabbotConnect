import os

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, APIRouter
from requests import Request
from starlette.responses import RedirectResponse

from apps.fastapi.auth.src import middlewares
from apps.fastapi.platform.modules.auth.src import auth_route
from apps.fastapi.platform.modules.core.src import core_route
from apps.fastapi.platform.modules.employees.src import employees_route
from libs.utils.common.custom_logger.src import (
    Colors,
    CustomLogger,
    LogType,
    color_string,
)
from libs.utils.common.os_helpers.src import BASE_DIR
from libs.utils.config.src.fastapi import GUNICORN_CONFIG_PATH

load_dotenv()

log = CustomLogger("HabbotConnect Backend App", queue_logger=True, is_request=False)
logger, listener = log.get_logger()
listener.start()

app = FastAPI(
    title="HabbotConnect Backend App",
    version="0.3.1",
    docs_url="/docs",
    redoc_url="/redoc",
    middleware=middlewares,
)


@app.exception_handler(404)
async def not_found_handler(_: Request, _exc):
    return RedirectResponse(url="/health")

api_router = APIRouter(prefix="/api")
api_router.include_router(core_route)
api_router.include_router(auth_route)
api_router.include_router(employees_route)


app.include_router(api_router)
def start_server(
    host: str,
    port: int,
    reload: bool = True,
    workers: int = 8,
    threads: int = 10,
    environment: str = "development",
):
    if environment == "development":
        logger.info(
            color_string(
                f"Starting server on http://{host}:{port}/docs with "
                f"{workers} workers, environment: {environment}, "
                f"reload: {reload}.",
                Colors.BOLD_RED,
            ),
            extra={"logType": LogType.STARTUP.value},
        )
        uvicorn.run(
            "apps.fastapi.src:app",
            host=host,
            port=port,
            reload=reload,
            log_level="info",
            workers=workers,
        )
    else:
        logger.info(
            color_string(
                f"Deploying server on http://{host}:{port}/docs with "
                f"{workers} workers, {threads} threads",
                Colors.BOLD_RED,
            ),
            extra={"logType": LogType.STARTUP.value},
        )
        os.system(f"gunicorn -c {BASE_DIR}/{GUNICORN_CONFIG_PATH} apps.fastapi.src:app")
