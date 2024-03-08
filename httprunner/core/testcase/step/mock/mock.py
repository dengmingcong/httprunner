from typing import Union

from httprunner.models import TStep, RawMockResponse


class MockMixin:
    """Mixin representing mock."""

    _step_context: TStep

    def mock(
        self, content: Union[dict, str], headers: dict = None, status_code: int = 200
    ):
        if headers is None:
            headers = {}
        self._step_context.request.raw_mock_response = RawMockResponse(
            content=content, headers=headers, status_code=status_code
        )
        return self
