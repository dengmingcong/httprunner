from typing import NoReturn, Optional

import allure
from loguru import logger

from httprunner.core.allure.runrequest.export_vars import save_extract_export_vars
from httprunner.core.allure.runrequest.http_session_data import save_http_session_data
from httprunner.core.allure.runrequest.validation_result import save_validation_result
from httprunner.core.runner.export_request_step_vars import export_extracted_variables
from httprunner.core.runner.retry import (
    gen_retry_step_title,
    is_meet_stop_retry_condition,
    is_final_request,
)
from httprunner.exceptions import RetryInterruptError, ValidationFailure
from httprunner.models import (
    SessionData,
    TStep,
    StepData,
)
from httprunner.response import ResponseObject


def save_run_request(
    session_data: SessionData,
    response_obj: ResponseObject,
    extract_mapping: dict,
    exported_vars: dict,
    is_export_extract_same,
) -> NoReturn:
    """Save RunRequest data to allure report."""
    try:
        save_http_session_data(session_data)
        save_validation_result(response_obj)
        save_extract_export_vars(extract_mapping, exported_vars, is_export_extract_same)
    except KeyError:
        logger.warning("Allure data was not saved.")


def save_run_request_retry(
    step: TStep,
    functions: dict,
    session_data: SessionData,
    response_obj: ResponseObject,
    step_data: StepData,
    extract_mapping: dict,
    session_variables: dict,
    content_size: int,
    exception: Optional[Exception],
) -> NoReturn:
    """Save RunRequest data to allure report."""
    if exception:
        is_pass = False
    else:
        is_pass = True

    # if retrying is needed and is_relay_export was set to False, do not export variables,
    # otherwise export variables.
    if not is_final_request(step, functions, exception) and not step.is_relay_export:
        is_export_extract_same = False
    else:
        is_export_extract_same = True
        export_extracted_variables(step_data, session_variables, extract_mapping)

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
                extract_mapping,
                step_data.export_vars,
                is_export_extract_same,
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
            extract_mapping,
            step_data.export_vars,
            is_export_extract_same,
        )

    # re-raise exception
    if exception:
        raise exception
