from typing import (
    Union,
)

from httprunner.core.testcase.config import Config  # noqa
from httprunner.core.testcase.step.runapi.request import HttpRunnerRequest
from httprunner.core.testcase.step.runrequest.export import StepRequestExport
from httprunner.core.testcase.step.runrequest.request.argument import (
    RequestWithOptionalArgs,
)
from httprunner.core.testcase.step.runrequest.response.extract import (
    StepRequestExtraction,
)
from httprunner.core.testcase.step.runrequest.response.validate import (
    StepRequestValidation,
)
from httprunner.core.testcase.step.runtestcase.refcase import StepRefCase
from httprunner.core.testcase.step.runtestcase.runtestcase import RunTestCase
from httprunner.models import (
    TStep,
    TRequest,
    TestCase,
)


class Step(object):
    def __init__(
        self,
        step_context: Union[
            HttpRunnerRequest,
            StepRequestValidation,
            StepRequestExtraction,
            StepRequestExport,
            RequestWithOptionalArgs,
            RunTestCase,
            StepRefCase,
        ],
    ):
        self._step_context = step_context.perform()

    @property
    def request(self) -> TRequest:
        return self._step_context.request

    @property
    def testcase(self) -> TestCase:
        return self._step_context.testcase  # noqa

    def perform(self) -> TStep:
        # fix: parametrized testcase always use the first parameter
        return self._step_context.model_copy(deep=True)
