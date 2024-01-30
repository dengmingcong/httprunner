from typing import (
    Text,
    Any,
    Optional,
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
        self.__resource_name = None  # type: Optional[str]
        self.__resource = None  # type: Optional[Any]
        self.__extractor = None  # type: Optional[str]

    def with_resource(
        self,
        name: str,
        resource: Any,
        extractor: Optional[str] = None,
    ) -> "RequestConfig":
        """
        Specify resource, extracting variables from the resource evaluated.

        :param name: name of the resource, one variable with the same name will be set,
            and its value is the evaluated resource.
        :param resource: resource to evaluate.
        :param extractor: extracting variables from the evaluated resource.
            The extracted variables will be set to the request config variables
            (have lower priority than those set by self.variables()).
            The value of this parameter must be a string and correspond to a debugtalk function.
        """
        self.__resource_name = name
        self.__resource = resource
        self.__extractor = extractor
        return self

    def variables(self, **variables) -> "RequestConfig":
        self.__variables.update(variables)
        return self

    def perform(self) -> TRequestConfig:
        return TRequestConfig(
            name=self.__name,
            variables=self.__variables,
            resource_name=self.__resource_name,
            resource=self.__resource,
            extractor=self.__extractor,
        )
