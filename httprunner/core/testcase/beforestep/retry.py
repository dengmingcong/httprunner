from typing import (
    Any,
    Union,
)

from httprunner.models import (
    TStep,
)


class RetryStepMixin:
    _step_context: TStep

    def retry_on_failure(
        self,
        retry_times: int,
        retry_interval: Union[int, float],
        stop_retry_if: Any = None,
    ):
        """
        Retry step until validation passed or max retries reached, or stop retry condition was met.

        :param retry_times: indicate max retried times
        :param retry_interval: sleep between each retry, unit: seconds
        :param stop_retry_if: stop retrying and mark step failed if the condition was met
        """
        self._step_context.remaining_retry_times = retry_times
        self._step_context.max_retry_times = retry_times
        self._step_context.retry_interval = retry_interval
        self._step_context.stop_retry_if = stop_retry_if
        return self
