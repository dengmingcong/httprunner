from httprunner.models import (
    TStep,
)


class StepVariableMixin(object):
    """Mixin representing setup for RunRequest."""

    _step_context: TStep

    def with_variables(self, **variables):
        self._step_context.variables.update(variables)
        return self

    def with_variables_raw(self, raw_variables: str, is_deep: bool = True):
        """
        Update step variables with raw_variables.

        :param raw_variables: the variables parsed from raw_variables will be updated to `step.variables`
        :param is_deep: `raw_variables` will be parsed twice if True
        """
        self._step_context.raw_variables = raw_variables
        self._step_context.is_deep_parse_raw_variables = is_deep
        return self
