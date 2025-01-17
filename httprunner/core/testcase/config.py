from copy import deepcopy
from typing import Text

from httprunner.models import StableDeepCopyDict, TConfig


class Config(object):
    def __init__(self, name: Text):
        self.__name = name
        self.__variables = StableDeepCopyDict()
        self.__base_url = ""
        self.__verify = False
        self.__continue_on_failure = False
        self.__export = []
        self.__weight = 1
        self.__path = None

    @property
    def name(self) -> Text:
        return self.__name

    @property
    def path(self) -> Text:
        return self.__path

    @path.setter
    def path(self, testcase_file_path: Text) -> None:
        self.__path = testcase_file_path

    @property
    def weight(self) -> int:
        return self.__weight

    def variables(self, **variables) -> "Config":
        self.__variables.update(variables)
        return self

    def base_url(self, base_url: Text) -> "Config":
        self.__base_url = base_url
        return self

    def verify(self, verify: bool) -> "Config":
        self.__verify = verify
        return self

    def continue_on_failure(self) -> "Config":
        self.__continue_on_failure = True
        return self

    def export(self, *export_var_name: Text) -> "Config":
        self.__export.extend(export_var_name)
        return self

    def locust_weight(self, weight: int) -> "Config":
        self.__weight = weight
        return self

    def perform(self) -> TConfig:
        return TConfig(
            name=self.__name,
            base_url=self.__base_url,
            verify=self.__verify,
            variables=deepcopy(
                self.__variables
            ),  # fix: variables are class attribute and will be shared
            export=list(set(self.__export)),
            path=self.__path,
            weight=self.__weight,
            continue_on_failure=self.__continue_on_failure,
        )
