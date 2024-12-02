import datetime
from zoneinfo import ZoneInfo

import allure

from httprunner.json_encoders import pydantic_model_dump_json
from httprunner.models import SessionData
from httprunner.pyproject import PyProjectToml


def save_http_session_data(
    http_session_data: SessionData,
) -> None:
    """Save http request and response to allure report."""
    # split session data into request, response, validation results, export vars, and stat if only one request exists
    if len(http_session_data.req_resps) == 1:
        request_data = http_session_data.req_resps[0].request
        response_data = http_session_data.req_resps[0].response

        # save request data
        if request_at_str := request_data.headers.get("Date", None):
            # Parse string to datetime object.
            request_at: datetime.datetime = datetime.datetime.fromisoformat(
                request_at_str
            )

            # Convert datetime object to target timezones.
            request_timezones_str = []
            for timezone_dict in PyProjectToml().request_timezones:
                # Format datetime object as specified timezone.
                timezone_format_string = request_at.astimezone(
                    ZoneInfo(timezone_dict["timezone"])
                ).strftime(timezone_dict["format"])

                # Add flag if it exists.
                if "flag" in timezone_dict:
                    timezone_format_string = (
                        f"{timezone_dict['flag']} {timezone_format_string}"
                    )

                request_timezones_str.append(timezone_format_string)

            # Join all formatted datetimes.
            request_timezones_str = " / ".join(request_timezones_str)

            request_attachment_name = (
                f"request 🕒 {request_timezones_str} / {request_at.timestamp()}"
            )
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
