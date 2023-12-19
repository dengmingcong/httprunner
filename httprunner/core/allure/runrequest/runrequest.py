from typing import NoReturn

from httprunner.core.allure.runrequest.export_vars import save_export_vars
from httprunner.core.allure.runrequest.http_session_data import save_http_session_data
from httprunner.core.allure.runrequest.validation_result import save_validation_result
from httprunner.models import (
    SessionData,
)
from httprunner.response import ResponseObject


def save_run_request(
    session_data: SessionData,
    response_obj: ResponseObject,
    exported_vars: dict,
) -> NoReturn:
    """Save RunRequest data to allure report."""
    save_http_session_data(session_data)
    save_validation_result(response_obj)
    save_export_vars(exported_vars)
