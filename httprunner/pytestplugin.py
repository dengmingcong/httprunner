import pytest

from httprunner import Config, HttpRunner


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
    parser.addoption(
        "--mock-mode",
        action="store_true",
        help="mock mode test",
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
def mock_mode(request, is_httprunner_test):
    """Continue running next steps if one step did not pass validation."""
    if not is_httprunner_test:
        return

    if request.config.getoption("--mock-mode"):
        config: Config = request.cls.config
        config.mock_mode()


@pytest.fixture(scope="function", autouse=True)
def clean_session_variables(request, is_httprunner_test):
    """Clean session variables before running test."""
    if not is_httprunner_test:
        return

    request.instance.with_variables({})
