from httprunner.core.testcase.config import Config  # noqa
from httprunner.core.testcase.step.hook.teardown import TeardownHookMixin
from httprunner.models import (
    TStep,
    StepExport,
)


class StepRefCase(TeardownHookMixin):
    def __init__(self, step_context: TStep):
        self._step_context = step_context

    def export(self, *var_names: str, **var_alias_mapping: str) -> "StepRefCase":
        """
        Export Variables from testcase referenced.

        :param var_names: each item of this list will be exported as is
        :param var_alias_mapping: key is the original variable name, value is the variable name that will be exported as
        """
        if not self._step_context.export:
            self._step_context.export = StepExport(
                var_names=var_names, var_alias_mapping=var_alias_mapping
            )
        else:
            # list.extend(Iterable), so pass in tuple is ok
            self._step_context.export.var_names.extend(var_names)
            self._step_context.export.var_alias_mapping.update(var_alias_mapping)
        return self

    def perform(self) -> TStep:
        return self._step_context
