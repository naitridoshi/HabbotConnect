import inspect
from datetime import datetime, timezone
from json import JSONDecodeError, loads

from starlette.concurrency import iterate_in_threadpool
from starlette.middleware import Middleware
from starlette.middleware.base import (
    BaseHTTPMiddleware,
    RequestResponseEndpoint,
)
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette_context import context, plugins
from starlette_context.middleware import RawContextMiddleware
from uvicorn.middleware.proxy_headers import ProxyHeadersMiddleware

from apps.fastapi.auth.src.helpers import decode_jwt_token
from libs.utils.common.custom_logger.src import CustomLogger
from libs.utils.common.custom_logger.src.helper import extra_details_for_req
from libs.utils.enums.src import TokenType

log = CustomLogger("AppMiddleware")

logger, listener = log.get_logger()
listener.start()


async def logging_iterator(response, iterator, class_name: str, start_time: datetime):
    response_body = dict()
    async for chunk in iterator:
        if loads(chunk.decode("utf-8")).get("is_final"):
            response_body = loads(chunk.decode("utf-8"))
        yield chunk
    extra = extra_details_for_req(
        inspect,
        class_name,
        response=response,
        response_body=response_body,
        start_time=start_time,
    )
    logger.info("✅ Streaming request completed successfully: ", extra=extra)


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint):
        excluded_paths = ["/"]

        if request.url.path in excluded_paths:
            return await call_next(request)

        start_time = datetime.now(timezone.utc)

        try:
            request_body = await request.json()
        except JSONDecodeError:
            request_body = dict()

        try:
            auth = request.headers.get("authorization")
            token = None

            if auth:
                parts = auth.split()

                if (
                    len(parts) == 2
                    and parts[0].lower() == TokenType.Bearer.value.lower()
                ):
                    token = parts[1]

            user_id = None
            if token:
                user_id = decode_jwt_token(token)

            context["userId"] = user_id
        except Exception as error:
            logger.warning(f"Error in decoding jwt token in middleware - {str(error)}")
            context["userId"] = None

        extra = extra_details_for_req(
            inspect, __class__.__name__, request, request_body
        )
        logger.info("🚀 Request initiated...", extra=extra)

        try:
            response = await call_next(request)
            if "text/event-stream" in response.headers["content-type"]:
                response.body_iterator = logging_iterator(
                    response=response,
                    iterator=response.body_iterator,
                    class_name=__class__.__name__,
                    start_time=start_time,
                )

            else:
                response_body = [chunk async for chunk in response.body_iterator]
                response.body_iterator = iterate_in_threadpool(iter(response_body))
                if response_body:
                    response_body = response_body[0].decode()
                else:
                    response_body = ""

                extra = extra_details_for_req(
                    inspect,
                    __class__.__name__,
                    response=response,
                    response_body=response_body,
                    start_time=start_time,
                )

                logger.info("✅ Request completed successfully", extra=extra)
        except Exception as error:
            response = JSONResponse(
                status_code=500, content={"success": False, "error": str(error)}
            )

            extra = extra_details_for_req(
                inspect,
                __class__.__name__,
                response=response,
                start_time=start_time,
            )
            logger.info("❌ Request failed...", extra=extra)

        return response


middlewares = [
    Middleware(
        ProxyHeadersMiddleware,
        trusted_hosts="*",  # Trust all hosts to properly extract client IP
    ),
    Middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc.)
        allow_headers=["*"],  # Allow all headers
    ),
    Middleware(
        RawContextMiddleware,
        plugins=[plugins.RequestIdPlugin(force_new_uuid=True)],
    ),
    Middleware(LoggingMiddleware),
]
