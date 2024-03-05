from typing import Union

from httprunner.models import (
    TStep,
)


class TimerMixin:
    """Mixin representing skipping step."""

    _step_context: TStep

    def with_pre_delay(self, seconds: Union[int, float, str]):
        """Delay before executing the step."""
        self._step_context.pre_delay = seconds
        return self

    def with_post_delay(self, seconds: Union[int, float, str]):
        """Delay after executing the step."""
        self._step_context.post_delay = seconds
        return self
