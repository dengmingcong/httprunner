from typing import (
    Callable,
)
from typing import (
    Text,
)

from httprunner.core.testcase.beforestep.param import ParametrizeStepMixin
from httprunner.core.testcase.beforestep.skip import SkipStepMixin
from httprunner.core.testcase.beforestep.timer import TimerMixin
from httprunner.core.testcase.beforestep.variable import StepVariableMixin
from httprunner.core.testcase.config import Config  # noqa
from httprunner.core.testcase.step.hook.setup import SetupHookMixin
from httprunner.core.testcase.step.runtestcase.refcase import StepRefCase
from httprunner.models import (
    TStep,
)


class RunTestCase(
    ParametrizeStepMixin,
    SkipStepMixin,
    SetupHookMixin,
    TimerMixin,
    StepVariableMixin,
):
    """
    Class entrypoint for a HttpRunner testcase.

    Note:
        RunTestCase does not support `retry_on_failure()`.
    """

    def __init__(self, name: Text):
        self._step_context = TStep(name=name)

    def call(self, testcase: Callable) -> StepRefCase:
        self._step_context.testcase = testcase
        return StepRefCase(self._step_context)

    def perform(self) -> TStep:
        return self._step_context
