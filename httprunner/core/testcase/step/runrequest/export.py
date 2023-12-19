from httprunner.core.testcase.config import Config  # noqa
from httprunner.core.testcase.step.runrequest.response.validate import (
    StepRequestValidation,
)

from httprunner.models import (
    TStep,
)


class StepRequestExport(object):
    def __init__(self, step_context: TStep):
        self._step_context = step_context

    def variable(
        self, step_var_name: str, export_as: str = None
    ) -> "StepRequestExport":
        """Make local step variables global for steps next."""
        if export_as:
            self._step_context.globalize.append({step_var_name: export_as})
        else:
            self._step_context.globalize.append(step_var_name)
        return self

    def validate(self) -> StepRequestValidation:
        return StepRequestValidation(self._step_context)

    def perform(self) -> TStep:
        return self._step_context
