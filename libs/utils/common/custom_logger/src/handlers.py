import json
import logging
import os
import sys
from datetime import datetime, timezone
from logging.handlers import RotatingFileHandler
from time import sleep

from pymsteams import connectorcard
from starlette.responses import JSONResponse
from starlette_context import context

from libs.utils.common.custom_logger.src.constants import (
    COLORS_DICT,
    color_for_log_level,
    webhook_url_for_logs,
)
from libs.utils.common.custom_logger.src.enums import LogType
from libs.utils.common.date_time.src import get_current_utc_timestamp
from libs.utils.common.os_helpers.src import BASE_DIR, get_relative_path
from libs.utils.config.src.logger import (
    MS_TEAMS_MESSAGE_RETRY_TIMEOUT_IN_SECONDS,
    MS_TEAMS_MESSAGE_SEND_RETRIES,
    MS_TEAMS_WEBHOOK_ENABLED,
)


class RequestDetailsFilter(logging.Filter):
    def __init__(self, is_request: bool = True, *args, **kwargs):
        self.is_request = is_request
        super().__init__(*args, **kwargs)

    def filter(self, record):
        record.requestId = "rid-None"
        record.userId = "uid-None"
        record.sessionId = "sid-None"
        if self.is_request:
            record.requestId = f"rid-{context.get('X-Request-ID', 'None')}"
            record.userId = f"uid-{context.get('userId', 'NEW_USER')}"
            record.sessionId = f"sid-{context.get('sessionId', 'None')}"

        return True


class TeamsHandler(logging.Handler):
    def __init__(self):
        super(TeamsHandler, self).__init__()

    def emit(self, record):
        try:
            send_to_teams = getattr(record, "sendInTeams", False)
            process_name = getattr(record, "name")
            log_level = getattr(record, "logLevel")
            message = getattr(record, "message")
            full_path = getattr(record, "pathname", None)
            if full_path:
                full_path = get_relative_path(full_path)

            lineno = getattr(record, "lineno")

            if not send_to_teams:
                return

            self.send_message_in_ms_teams(
                process_name, log_level, message, full_path, lineno
            )
        except Exception as error:
            print(f"Error sending log message to Teams: {error}")

    def send_message_in_ms_teams(
        self,
        process_name: str,
        log_level: str,
        message: str,
        full_path: str,
        lineno: str,
    ):
        message = self._format_log(process_name, message, full_path, lineno)

        if not MS_TEAMS_WEBHOOK_ENABLED:
            return

        for _ in range(MS_TEAMS_MESSAGE_SEND_RETRIES):
            try:
                log_level = log_level.upper()
                message_obj = connectorcard(webhook_url_for_logs[log_level])
                message_obj.color(color_for_log_level[log_level])
                message_obj.text(message)
                message_obj.send()
                break
            except Exception as error:
                print("Error in sending log message to Teams:", error)
                sleep(MS_TEAMS_MESSAGE_RETRY_TIMEOUT_IN_SECONDS)

    @staticmethod
    def _format_log(process_name: str, message: str, full_path: str, lineno: str):
        log_obj = {
            "process": process_name,
            "message": message,
            "fullPath": full_path,
            "lineNo": lineno,
            "auditAt": get_current_utc_timestamp(),
        }

        return f"<pre>{json.dumps(log_obj, indent=4)}</pre>"


# Custom formatter to add colors
class ColoredFormatter(logging.Formatter):
    def format(self, record):
        record = self.__format_record(record)

        colors = {
            "logLevel": COLORS_DICT.get(record.logLevel, COLORS_DICT["RESET"]),
            "logType": COLORS_DICT.get(record.logType, COLORS_DICT["RESET"]),
            "auditAt": COLORS_DICT.get("AUDIT_AT", COLORS_DICT["RESET"]),
            "requestId": COLORS_DICT.get("REQUEST_ID"),
            "sessionId": COLORS_DICT.get("SESSION_ID"),
            "userId": COLORS_DICT.get("USER_ID"),
            "qualname": COLORS_DICT.get("QUAL_NAME"),
        }
        colored_attrs = {
            attr: f"{colors[attr]}{getattr(record, attr)}{COLORS_DICT['RESET']}"
            for attr in colors
            if hasattr(record, attr)
        }

        formatted_record = super().format(record)

        for attr, colored_value in colored_attrs.items():
            if getattr(record, attr, None):
                formatted_record = formatted_record.replace(
                    str(getattr(record, attr)), colored_value
                )

        return formatted_record

    @staticmethod
    def __format_record(record):
        record_dict = record.__dict__

        record.auditAt = str(
            datetime.fromtimestamp(record_dict.get("created"), timezone.utc)
        )
        record.logLevel = record_dict.get("levelname")
        record.logType = record_dict.get("logType", LogType.DEFAULT.value)
        record.extraDetails = record_dict.get("extraDetails", "")
        function_name = record_dict.get("functionName", None)
        if function_name is None:
            function_name = record_dict.get("funcName", "N/A")

        class_name = record_dict.get("className", None)
        if class_name is None:
            class_name = record_dict.get("name")

        record.qualname = f"{class_name}.{function_name}"

        return record


class DynamicFileHandler(RotatingFileHandler):
    def __init__(self, *args, **kwargs):
        self.base_directory = os.path.join(BASE_DIR, "logs")
        os.makedirs(self.base_directory, exist_ok=True)
        # Initialize with a default file
        super().__init__(
            os.path.join(self.base_directory, "history.log"), *args, **kwargs
        )


class CustomJsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        record_dict = record.__dict__.copy()
        serializable_record_dict = {
            key: self.make_json_serializable(value)
            for key, value in record_dict.items()
        }
        return json.dumps(serializable_record_dict)

    @staticmethod
    def make_json_serializable(value):
        if isinstance(value, dict):
            return {
                k: CustomJsonFormatter.make_json_serializable(v)
                for k, v in value.items()
                if v is not None
            }
        elif isinstance(value, list):
            return [
                CustomJsonFormatter.make_json_serializable(v)
                for v in value
                if v is not None
            ]
        elif isinstance(value, JSONResponse):
            return {
                "status_code": value.status_code,
                "headers": dict(value.headers),
                "body": (
                    value.body.decode("utf-8")
                    if isinstance(value.body, bytes)
                    else value.body
                ),
            }
        elif isinstance(value, (int, float, str, bool)) or value is None:
            return value
        else:
            return str(value)


# Create formatter
console_format = ColoredFormatter(
    fmt=" ".join(
        [
            "%(auditAt)s |",
            "%(logLevel)s |",
            "%(userId)s |",
            "%(requestId)s |",
            "%(sessionId)s |",
            "%(logType)s |",
            "%(qualname)s |",
            "%(message)s |",
            "%(extraDetails)s.",
        ]
    )
)
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(console_format)

dynamic_file_handler = DynamicFileHandler(
    maxBytes=1 * 1024 * 50, backupCount=10, encoding="utf-8"
)
json_formatter = CustomJsonFormatter()
dynamic_file_handler.setFormatter(json_formatter)


if MS_TEAMS_WEBHOOK_ENABLED:
    teams_handler = TeamsHandler()
    teams_handler.setLevel(logging.DEBUG)
else:
    teams_handler = None
