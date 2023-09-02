from pathlib import Path
from typing import NoReturn

from _pytest.config.findpaths import get_common_ancestor, get_dirs_from_args
from _pytest.pathlib import absolutepath


class ArgParser:
    def __init__(self):
        self.__pytest_config = None
        self.__test_path = None

    @property
    def pytest_config(self):
        """Get pytest config."""
        return self.__pytest_config

    @pytest_config.setter
    def pytest_config(self, pytest_config):
        """Set pytest config."""
        self.__pytest_config = pytest_config

    @property
    def test_path(self) -> Path:
        """Get test path parsed from pytest args."""
        if self.__test_path is None:
            self._set_test_path_on_config()

        return self.__test_path

    def _set_test_path_on_config(self) -> NoReturn:
        """Set test path on pytest config."""
        if self.pytest_config is None:
            raise AttributeError("attribute `pytest_config` is not set yet.")

        # load debugtalk functions from `FILE` specified by option instead of trying to locate one debugtalk.py file
        if debugtalk_py_file := self.__pytest_config.getoption("--debugtalk-py-file"):
            debugtalk_py_file = absolutepath(debugtalk_py_file)

            if not debugtalk_py_file.is_file():
                raise FileNotFoundError(
                    f"debugtalk.py file not found: {debugtalk_py_file}"
                )

            self.__test_path = debugtalk_py_file
        else:
            # locate common ancestor directory of all test files
            # and search recursively upwards to find debugtalk.py file
            # WARNING: if operation `chdir` is called in test file, this method may not work as expected and
            # need to call `load_project_meta` manually in test file and set `reload` to True.
            dirs = get_dirs_from_args(self.__pytest_config.args)
            self.__test_path = get_common_ancestor(dirs)


arg_parser = ArgParser()
