import pytest
from _pytest.config.findpaths import get_common_ancestor, get_dirs_from_args
from _pytest.pathlib import absolutepath

from httprunner import Config, HttpRunner
from httprunner.loader import load_project_meta


def pytest_addoption(parser):
    """
    Provide custom pytest options.
    """
    parser.addoption(
        "--continue-on-failure",
        action="store_true",
        help="next steps will continue running if one step did not pass validation",
    )
    parser.addoption(
        "--debugtalk-py-file",
        action="store",
        help="load debugtalk functions from `FILE` instead of trying to locate one debugtalk.py file",
    )


@pytest.fixture
def is_httprunner_test(request) -> bool:
    """
    Return True if request test is a HttpRunner test.
    """
    if request.instance and isinstance(request.instance, HttpRunner):
        return True
    else:
        return False


@pytest.fixture(scope="function", autouse=True)
def continue_on_failure(request, is_httprunner_test):
    """Continue running next steps if one step did not pass validation."""
    if not is_httprunner_test:
        return

    if request.config.getoption("--continue-on-failure"):
        config: Config = request.cls.config
        config.continue_on_failure()


@pytest.fixture(scope="function", autouse=True)
def clean_session_variables(request, is_httprunner_test):
    """Clean session variables before running test."""
    if not is_httprunner_test:
        return

    request.instance.with_variables({})


def pytest_sessionstart(session):
    """
    Called after the Session object has been created and before performing collection and entering the run test loop.
    """
    # load debugtalk functions from `FILE` specified by option instead of trying to locate one debugtalk.py file
    if debugtalk_py_file := session.config.getoption("--debugtalk-py-file"):
        debugtalk_py_file = absolutepath(debugtalk_py_file)

        if not debugtalk_py_file.is_file():
            raise FileNotFoundError(f"debugtalk.py file not found: {debugtalk_py_file}")

        load_project_meta(debugtalk_py_file.as_posix())
    else:
        # locate common ancestor directory of all test files and search recursively upwards to find debugtalk.py file
        dirs = get_dirs_from_args(session.config.args)
        common_ancestor = get_common_ancestor(dirs)
        load_project_meta(common_ancestor.as_posix())
