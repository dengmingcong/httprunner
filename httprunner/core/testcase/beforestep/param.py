from typing import (
    Union,
    Iterable,
    Sequence,
    Optional,
)

from httprunner.models import (
    TStep,
)


class ParametrizeStepMixin:
    """Resolve and generate real steps."""

    _step_context: TStep

    def parametrize(
        self,
        argnames: str,
        argvalues: Union[str, Iterable[Union[Sequence[object], object]]],
        ids: Optional[Union[str, Iterable]] = None,
        *,
        is_skip_empty_parameter: bool = True,
        is_keep_export_history: bool = False
    ):
        """
        Parametrize step.

        :param argnames: A comma-separated string denoting one or more argument names
        :param argvalues: If only one argname was specified argvalues is a list of values.
            If N argnames were specified, argvalues must be a list of N-tuples, where each tuple-element
            specifies a value for its respective argname.
        :param ids: Sequence of ids for argvalues.
        :param is_skip_empty_parameter: skip steps with an empty parameter set
        :param is_keep_export_history: if need to keep export history. note: not supported export alias
        """
        self._step_context.parametrize = (
            argnames,
            argvalues,
            ids,
            is_skip_empty_parameter,
            is_keep_export_history,
        )
        return self
