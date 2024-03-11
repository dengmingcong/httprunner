from typing import (
    Text,
    Union,
)

from httprunner.core.testcase.beforestep.param import ParametrizeStepMixin
from httprunner.core.testcase.beforestep.retry import RetryStepMixin
from httprunner.core.testcase.beforestep.skip import SkipStepMixin
from httprunner.core.testcase.beforestep.timer import TimerMixin
from httprunner.core.testcase.beforestep.variable import StepVariableMixin
from httprunner.core.testcase.config import Config  # noqa
from httprunner.core.testcase.step.hook.setup import SetupHookMixin
from httprunner.core.testcase.step.runapi.config import RequestConfig
from httprunner.core.testcase.step.runrequest.request.argument import (
    RequestWithOptionalArgs,
)
from httprunner.core.testcase.step.runrequest.response.extract import (
    StepRequestExtraction,
)
from httprunner.core.testcase.step.runrequest.response.validate import (
    StepRequestValidation,
)
from httprunner.models import (
    TStep,
    StableDeepCopyDict,
)


class HttpRunnerRequest(
    ParametrizeStepMixin,
    SkipStepMixin,
    RetryStepMixin,
    StepVariableMixin,
    SetupHookMixin,
    TimerMixin,
    RequestWithOptionalArgs,
):
    """
    Class representing a HttpRunner request.

    The class attribute 'request' will be used as the default TStep.
    """

    config: RequestConfig
    request: Union[
        RequestWithOptionalArgs, StepRequestValidation, StepRequestExtraction
    ]

    def __init_subclass__(cls):
        """Add validation for subclasses."""
        super().__init_subclass__()

        # make sure type of class attributes correct
        if not isinstance(cls.config, RequestConfig):
            raise ValueError("type of request config must be RequestConfig")

        # make sure TStep.request exist and is not None
        if not isinstance(
            cls.request,
            (RequestWithOptionalArgs, StepRequestValidation, StepRequestExtraction),
        ):
            raise ValueError(
                "type of request must be one of "
                "RequestWithOptionalArgs, StepRequestValidation, or StepRequestExtraction"
            )

    def __init__(self, name: Text = None):  # noqa
        # refer to the copy of class attribute 'request' as the default TStep
        # note: copy() is required for class attribute are shared among instances and code below will change the `step`
        step = self.request.perform().model_copy(deep=True)  # type: TStep

        # move variables from step.variables to step.private_variables
        step.private_variables = step.variables
        step.variables = StableDeepCopyDict()
        self._step_context = step

        # update name with data of config
        self.__config = self.config.perform()
        self._step_context.name = self.__config.name
        # overwrite name with instance attribute 'name' if existed
        if name:
            self._step_context.name = name

        # save request config for later usage: testcase config variables > request config variables
        self._step_context.request_config = self.__config

    def perform(self) -> TStep:
        return self._step_context
