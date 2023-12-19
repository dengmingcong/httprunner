from httprunner.models import TStep


class BaseStep:
    """Base class for all steps."""

    def __init__(self, name: str):
        self._step_context = TStep(name=name)
