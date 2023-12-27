from typing import NoReturn, Optional

import allure
from loguru import logger

from httprunner.core.allure.runrequest.export_vars import save_export_vars
from httprunner.core.allure.runrequest.http_session_data import save_http_session_data
from httprunner.core.allure.runrequest.validation_result import save_validation_result
from httprunner.core.runner.retry import (
    gen_retry_step_title,
    is_meet_stop_retry_condition,
)
from httprunner.exceptions import RetryInterruptError, ValidationFailure
from httprunner.models import (
    SessionData,
    TStep,
)
from httprunner.response import ResponseObject


def save_run_request(
    session_data: SessionData,
    response_obj: ResponseObject,
    exported_vars: dict,
) -> NoReturn:
    """Save RunRequest data to allure report."""
    try:
        save_http_session_data(session_data)
        save_validation_result(response_obj)
        save_export_vars(exported_vars)
    except KeyError:
        logger.warning("Allure data was not saved.")


def save_run_request_retry(
    step: TStep,
    functions: dict,
    session_data: SessionData,
    response_obj: ResponseObject,
    exported_vars: dict,
    content_size: int,
    exception: Optional[Exception],
) -> NoReturn:
    """Save RunRequest data to allure report."""
    if exception:
        is_pass = False
    else:
        is_pass = True

    if step.is_ever_retried:
        # success will stop retrying automatically.
        # stopping retrying only happens when ValidationFailure is raised.
        if (
            not is_pass
            and isinstance(exception, ValidationFailure)
            and is_meet_stop_retry_condition(step, functions)
        ):
            is_stop_retry = True
        else:
            is_stop_retry = False

        step_title = gen_retry_step_title(
            step,
            is_pass,
            content_size,
            is_stop_retry,
        )
        with allure.step(step_title):
            save_run_request(
                session_data,
                response_obj,
                exported_vars,
            )
            if not is_pass:
                # mark step as failed in allure if this is the last retry and exception was raised
                if step.remaining_retry_times == 0:
                    raise exception

                # mark step as failed in allure if stopping retrying condition was met and exception was raised
                if is_stop_retry:
                    raise RetryInterruptError(exception)
    else:
        save_run_request(
            session_data,
            response_obj,
            exported_vars,
        )

    # re-raise exception
    if exception:
        raise exception
