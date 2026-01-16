from typing import Any, Dict, Optional


def success_response(data: Any = None, message: Optional[str] = None) -> Dict[str, Any]:
    response: Dict[str, Any] = {"success": True}

    if message:
        response["message"] = message
    if data is not None:
        response["data"] = data

    return response
