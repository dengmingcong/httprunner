import pytest

from httprunner import Config, HttpRunner
from httprunner.argparser import arg_parser


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


def pytest_cmdline_main(config):
    """
    Set test path on pytest config.

    Notes for hook self:
        Called for performing the main command line action.

        The default implementation will invoke the configure hooks and runtest_mainloop.

        Stops at first non-None result.
    """
    arg_parser.pytest_config = config
