from typing import (
    Text,
)

from httprunner.core.testcase.config import Config  # noqa
from httprunner.models import (
    TRequestConfig,
    StableDeepCopyDict,
)


class RequestConfig(object):
    """Class representing request config."""

    def __init__(self, name: Text):
        self.__name = name
        self.__variables = StableDeepCopyDict()

    def variables(self, **variables) -> "RequestConfig":
        self.__variables.update(variables)
        return self

    def perform(self) -> TRequestConfig:
        return TRequestConfig(
            name=self.__name,
            variables=self.__variables,
        )
