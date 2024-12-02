from typing import Optional, Union

from httprunner.models import TStep


class TimerMixin:
    """Mixin representing skipping step."""

    _step_context: TStep

    def with_pre_delay(
        self, seconds: Union[int, float, str], reason: Optional[str] = None
    ):
        """Delay (in seconds) before executing the step.

        :param seconds: Seconds to delay.
        :param reason: Why the delay is needed.
        """
        self._step_context.pre_delay_seconds = seconds
        self._step_context.pre_delay_reason = reason
        return self

    def with_post_delay(
        self, seconds: Union[int, float, str], reason: Optional[str] = None
    ):
        """Delay (in seconds) after executing the step.

        :param seconds: Seconds to delay.
        :param reason: Why the delay is needed.
        """
        self._step_context.post_delay_seconds = seconds
        self._step_context.post_delay_reason = reason
        return self
