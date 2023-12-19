from typing import NoReturn

import allure

from httprunner.json_encoders import (
    pydantic_model_dump_json,
)
from httprunner.models import (
    SessionData,
)


def save_http_session_data(
    http_session_data: SessionData,
) -> NoReturn:
    """Save http request and response to allure report."""
    # split session data into request, response, validation results, export vars, and stat if only one request exists
    if len(http_session_data.req_resps) == 1:
        request_data = http_session_data.req_resps[0].request
        response_data = http_session_data.req_resps[0].response

        # save request data
        if request_at := request_data.headers.get("Date", None):
            request_attachment_name = f"request 🕒 {request_at}"
        else:
            request_attachment_name = "request"
        allure.attach(
            pydantic_model_dump_json(request_data, indent=4),
            request_attachment_name,
            allure.attachment_type.JSON,
        )

        # save response data
        allure.attach(
            pydantic_model_dump_json(response_data, indent=4),
            "response",
            allure.attachment_type.JSON,
        )

        # save stat
        allure.attach(
            pydantic_model_dump_json(http_session_data.stat, indent=4),
            "statistics",
            allure.attachment_type.JSON,
        )
    else:
        # put request, response, and validation results in one attachment
        allure.attach(
            pydantic_model_dump_json(http_session_data, indent=4),
            "session data",
            allure.attachment_type.JSON,
        )
