from typing import (
    Text,
)

from httprunner.core.testcase.config import Config  # noqa
from httprunner.core.testcase.step.runrequest.request.argument import (
    RequestWithOptionalArgs,
)
from httprunner.models import (
    TRequest,
    MethodEnum,
    TStep,
)


class HttpMethodMix:
    """Mixin representing HTTP methods."""

    _step_context: TStep

    def get(self, url: Text) -> RequestWithOptionalArgs:
        self._step_context.request = TRequest(method=MethodEnum.GET, url=url)
        return RequestWithOptionalArgs(self._step_context)

    def post(self, url: Text) -> RequestWithOptionalArgs:
        self._step_context.request = TRequest(method=MethodEnum.POST, url=url)
        return RequestWithOptionalArgs(self._step_context)

    def put(self, url: Text) -> RequestWithOptionalArgs:
        self._step_context.request = TRequest(method=MethodEnum.PUT, url=url)
        return RequestWithOptionalArgs(self._step_context)

    def head(self, url: Text) -> RequestWithOptionalArgs:
        self._step_context.request = TRequest(method=MethodEnum.HEAD, url=url)
        return RequestWithOptionalArgs(self._step_context)

    def delete(self, url: Text) -> RequestWithOptionalArgs:
        self._step_context.request = TRequest(method=MethodEnum.DELETE, url=url)
        return RequestWithOptionalArgs(self._step_context)

    def options(self, url: Text) -> RequestWithOptionalArgs:
        self._step_context.request = TRequest(method=MethodEnum.OPTIONS, url=url)
        return RequestWithOptionalArgs(self._step_context)

    def patch(self, url: Text) -> RequestWithOptionalArgs:
        self._step_context.request = TRequest(method=MethodEnum.PATCH, url=url)
        return RequestWithOptionalArgs(self._step_context)
