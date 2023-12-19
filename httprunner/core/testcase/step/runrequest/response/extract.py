from typing import (
    Text,
    Callable,
)

from httprunner.core.testcase.config import Config  # noqa
from httprunner.core.testcase.step.runrequest.export import StepRequestExport
from httprunner.core.testcase.step.runrequest.response.validate import (
    StepRequestValidation,
)
from httprunner.models import (
    TStep,
    JMESPathExtractor,
)


class StepRequestExtraction(object):
    """Class representing response extraction."""

    def __init__(self, step_context: TStep):
        self._step_context = step_context

    def clear(self) -> "StepRequestExtraction":
        """Clear extractors already added."""
        self._step_context.extract = []
        return self

    def with_jmespath(
        self, jmespath_expression: Text, var_name: Text, sub_extractor: Callable = None
    ) -> "StepRequestExtraction":
        self._step_context.extract.append(
            JMESPathExtractor(
                variable_name=var_name,
                expression=jmespath_expression,
                sub_extractor=sub_extractor,
            )
        )
        return self

    # def with_regex(self):
    #     # TODO: extract response html with regex
    #     pass
    #
    # def with_jsonpath(self):
    #     # TODO: extract response json with jsonpath
    #     pass

    def export(self) -> StepRequestExport:
        return StepRequestExport(self._step_context)

    def validate(self) -> StepRequestValidation:
        return StepRequestValidation(self._step_context)

    def perform(self) -> TStep:
        return self._step_context
