from typing import NoReturn

import allure
from loguru import logger

from httprunner.client import HttpSession
from httprunner.configs.emoji import emojis
from httprunner.core.allure.runrequest.runrequest import save_run_request
from httprunner.response import ResponseObject


def save_run_request_retry(
    session: HttpSession,
    response_obj: ResponseObject,
    exported_vars: dict,
    max_retry_times: int,
    remaining_retry_times: int,
    is_meet_stop_retry_condition: bool = False,
) -> NoReturn:
    """
    Save RunRequest data to allure report.

    Note:
        1. this function is exclusively used for method self.__run_step_request().
        2. if retry is needed (max_retries > 0), add new allure step as context
    """
    if not hasattr(session, "data"):
        return

    if max_retry_times > 0:
        if session.data.success:
            result = emojis.success
        else:
            result = emojis.failure

        if max_retry_times == remaining_retry_times:
            title = f"first request {result}"
        elif remaining_retry_times == 0:
            title = f"retry: {max_retry_times} - last retry {result}"
        else:
            title = f"retry: {max_retry_times - remaining_retry_times} {result}"

        if is_meet_stop_retry_condition:
            title += " (the condition to stop retrying was met)"

        # display Content-Length of response in title
        try:
            title += (
                f'  • Content-Length: {response_obj.resp_obj.headers["Content-Length"]}'
            )
        except Exception as e:
            logger.warning(
                f"error occurred while extracting content-length from response, exception: {repr(e)}"
            )

        with allure.step(title):
            save_run_request(session.data, response_obj, exported_vars)
    else:
        save_run_request(session.data, response_obj, exported_vars)
