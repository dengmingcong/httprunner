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
        self.__api = None  # type: Optional[Any]
        self.__variable_extractor = None  # type: Optional[str]
        self.__preset_json_extractor = None  # type: Optional[str]

    def with_api(
        self,
        api: Any,
        variable_extractor: str,
        preset_json_extractor: str,
    ) -> "RequestConfig":
        """
        Specify api, extracting variables and preset json from the api evaluated.

        :param api: api to evaluate. A variable named 'api' will be set and its value is the evaluated api.
        :param variable_extractor: extracting variables from the evaluated api.
            The extracted variables will be set to the request config variables
            (have lower priority than those set by self.variables()).
            The value of this parameter must be a string and correspond to a debugtalk function.
        :param preset_json_extractor: extracting preset json from the evaluated api.
            A variable named 'preset_json' will be set and its value is the extracted preset json.
            The value of this parameter must be a string and correspond to a debugtalk function.
        """
        self.__api = api
        self.__variable_extractor = variable_extractor
        self.__preset_json_extractor = preset_json_extractor
        return self

    def variables(self, **variables) -> "RequestConfig":
        self.__variables.update(variables)
        return self

    def perform(self) -> TRequestConfig:
        return TRequestConfig(
            name=self.__name,
            variables=self.__variables,
            api=self.__api,
            variable_extractor=self.__variable_extractor,
            preset_json_extractor=self.__preset_json_extractor,
        )
