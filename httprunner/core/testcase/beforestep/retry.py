from typing import (
    Any,
)

from httprunner.models import (
    TStep,
)


class RetryStepMixin:
    """Mixin representing retrying step."""

    _step_context: TStep

    def retry_on_failure(
        self,
        retry_times: Any,
        retry_interval: Any,
        stop_retry_if: Any = None,
        is_relay_export: bool = False,
    ):
        """
        Retry step until validation passed or max retries reached, or stop retry condition was met.

        :param retry_times: indicate max retried times
        :param retry_interval: sleep between each retry, unit: seconds
        :param stop_retry_if: stop retrying and mark step failed if the condition was met
        :param is_relay_export: whether to export extracted variables when in retrying progress
        """
        self._step_context.remaining_retry_times = retry_times
        self._step_context.max_retry_times = retry_times
        self._step_context.retry_interval = retry_interval
        self._step_context.stop_retry_if = stop_retry_if
        self._step_context.is_relay_export = is_relay_export
        return self
