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
        :param is_keep_export_history:
            如果为 True，会将参数化步骤每一步的导出变量添加 _{id} 后缀的同时导出。
            注意：
            1. 如果 .export 方法使用了导出别名的形式，var_name=var_name_alias，var_name 和 var_name_alias 变量都不会添加后缀导出。
            2. 如果 .export 方法 var_name 和 var_alias_mapping 都使用了，且包含同一个变量名，那么别名会被添加了后缀的变量名覆盖然后导出。
        """
        self._step_context.parametrize = (
            argnames,
            argvalues,
            ids,
            is_skip_empty_parameter,
            is_keep_export_history,
        )
        return self
