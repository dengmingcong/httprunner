from httprunner.models import TStep


class MockMixin:
    """Mixin representing mock."""

    _step_context: TStep

    def mock(self, mock_body=None):
        self._step_context.mock_body = mock_body

        return self
