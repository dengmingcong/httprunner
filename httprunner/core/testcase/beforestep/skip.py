from typing import (
    Any,
)

from httprunner.models import (
    TStep,
)


class SkipStepMixin:
    """Mixin representing skipping step."""

    _step_context: TStep

    def skip_if(self, condition: Any, reason: str = None):
        self._step_context.skip_if_condition = condition
        self._step_context.skip_reason = reason
        return self

    def skip_unless(self, condition: Any, reason: str = None):
        self._step_context.skip_unless_condition = condition
        self._step_context.skip_reason = reason
        return self
