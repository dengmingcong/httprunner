from typing import (
    Text,
)

from httprunner.core.testcase.beforestep.param import ParametrizeStepMixin
from httprunner.core.testcase.beforestep.retry import RetryStepMixin
from httprunner.core.testcase.beforestep.skip import SkipStepMixin
from httprunner.core.testcase.beforestep.variable import StepVariableMixin
from httprunner.core.testcase.step.base import BaseStep
from httprunner.core.testcase.step.hook.setup import SetupHookMixin
from httprunner.core.testcase.step.runrequest.request.method import HttpMethodMix


class RunRequest(
    BaseStep,
    ParametrizeStepMixin,
    SkipStepMixin,
    RetryStepMixin,
    StepVariableMixin,
    SetupHookMixin,
    HttpMethodMix,
):
    """Class entrypoint for a HttpRunner request."""

    def __init__(self, name: Text):
        super().__init__(name)
