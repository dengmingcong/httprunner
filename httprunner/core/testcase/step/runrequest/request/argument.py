from typing import (
    Union,
)

from httprunner.builtin import update_dict_recursively
from httprunner.core.testcase.step.hook.teardown import TeardownHookMixin
from httprunner.core.testcase.step.runrequest.export import StepRequestExport
from httprunner.core.testcase.step.runrequest.response.extract import (
    StepRequestExtraction,
)
from httprunner.core.testcase.step.runrequest.response.validate import (
    StepRequestValidation,
)
from httprunner.models import (
    TStep,
)


class RequestWithOptionalArgs(TeardownHookMixin):
    """Mixin representing arguments for RunRequest."""

    def __init__(self, step_context: TStep):
        self._step_context = step_context

    def with_origin(self, origin: str) -> "RequestWithOptionalArgs":
        """
        Specify actual origin.

        Origin specified by HTTP method or config.base_url will be substituted by this value.
        """
        self._step_context.request.origin = origin
        return self

    def with_params(self, **params) -> "RequestWithOptionalArgs":
        self._step_context.request.params.update(params)
        return self

    def with_headers(self, **headers) -> "RequestWithOptionalArgs":
        self._step_context.request.headers.update(headers)
        return self

    def with_cookies(self, **cookies) -> "RequestWithOptionalArgs":
        self._step_context.request.cookies.update(cookies)
        return self

    def with_data(self, data) -> "RequestWithOptionalArgs":
        self._step_context.request.data = data
        return self

    def with_json(self, req_json) -> "RequestWithOptionalArgs":
        self._step_context.request.req_json = req_json
        return self

    def update_json_object(
        self,
        req_json_update: Union[dict, str],
        is_deep: bool = True,
        is_update_before_parse: bool = True,
    ) -> "RequestWithOptionalArgs":
        """
        Update request.req_json.

        Note:
            call `with_json()` first before calling this method, otherwise an exception will be raised

        :param req_json_update: the data to update with
        :param is_deep: update recursively if True
        :param is_update_before_parse: update `req_json` with `req_json_update` and then parse the result if True,
            this argument only takes effect if both `req_json` and `req_json_update` are dict
        """
        if self._step_context.request.req_json is None:
            self._step_context.request.req_json = {}

        if is_update_before_parse:
            # apply update if both are dict to avoid parsing error
            if isinstance(self._step_context.request.req_json, dict) and isinstance(
                req_json_update, dict
            ):
                if is_deep:
                    update_dict_recursively(
                        self._step_context.request.req_json, req_json_update
                    )
                else:
                    self._step_context.request.req_json.update(req_json_update)
            else:
                self._step_context.request.req_json_update.append(
                    (req_json_update, is_deep)
                )
        else:
            self._step_context.request.req_json_update.append(
                (req_json_update, is_deep)
            )

        return self

    def update_form_data(
        self,
        data_update: Union[dict, str],
        is_deep: bool = True,
        is_update_before_parse: bool = True,
    ) -> "RequestWithOptionalArgs":
        """
        Update 'request.data' if 'request.data' is a JSON object.

        Note:
            call `with_data()` first before calling this method, otherwise an exception will be raised

        :param data_update: the data to update with
        :param is_deep: update recursively if True
        :param is_update_before_parse: update `data` with `data_update` and then parse the result if True,
            this argument only takes effect if both `data` and `data_update` are dict
        """
        if self._step_context.request.data is None:
            self._step_context.request.data = {}

        if is_update_before_parse:
            # apply update if both are dict to avoid parsing error
            if isinstance(self._step_context.request.data, dict) and isinstance(
                data_update, dict
            ):
                if is_deep:
                    update_dict_recursively(
                        self._step_context.request.data, data_update
                    )
                else:
                    self._step_context.request.data.update(data_update)
            else:
                self._step_context.request.data_update.append((data_update, is_deep))
        else:
            self._step_context.request.data_update.append((data_update, is_deep))

        return self

    def set_timeout(self, timeout: float) -> "RequestWithOptionalArgs":
        self._step_context.request.timeout = timeout
        return self

    def set_verify(self, verify: bool) -> "RequestWithOptionalArgs":
        self._step_context.request.verify = verify
        return self

    def set_allow_redirects(self, allow_redirects: bool) -> "RequestWithOptionalArgs":
        self._step_context.request.allow_redirects = allow_redirects
        return self

    def upload(self, **file_info) -> "RequestWithOptionalArgs":
        self._step_context.request.upload.update(file_info)
        return self

    def extract(self) -> StepRequestExtraction:
        return StepRequestExtraction(self._step_context)

    def export(self) -> StepRequestExport:
        return StepRequestExport(self._step_context)

    def validate(self) -> StepRequestValidation:
        return StepRequestValidation(self._step_context)

    def perform(self) -> TStep:
        return self._step_context
