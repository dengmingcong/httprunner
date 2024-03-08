from httprunner.models import TStep


class MockMixin:
    """Mixin representing mock."""

    _step_context: TStep

    def mock(self, mock_body=None):
        if mock_body is None:
            mock_body = {}
        self._step_context.mock_body = mock_body

        return self
