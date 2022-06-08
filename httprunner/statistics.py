"""
Retrieve stat info.
"""
from httprunner.models import StepData, SessionData
from httprunner.runner import HttpRunner


def get_session_data_stat(session_data: SessionData) -> dict:
    """
    Retrieve stat info from session data.

    Usually one session data only contains one request,
    but it may also contain multiple requests when redirection is required.

    >>> get_session_data_stat(...)
    {
        "success": True,
        "elapsed": 100,
        "url": "http://www.example.com"
    }

    or

    {
        "success": True,
        "elapsed": 100,
        "urls": ["http://www.foo.com", "http://www.bar.com"]
    }
    """
    stat_info = {
        "success": session_data.success,
        "elapsed": session_data.stat.response_time_ms,
    }
    if (length := len(session_data.req_resps)) == 1:
        stat_info["url"] = session_data.req_resps[0].request.url
    elif length > 1:
        stat_info["urls"] = [_.request.url for _ in session_data.req_resps]
    else:
        stat_info["url"] = "NA"

    return stat_info


def get_step_data_stat(step_data: StepData):
    """
    Retrieve stat info from step data.

    A step data may contain a list of other step datas.

    >>> get_step_data_stat(...)
    {
        "name": "foo",
        "success": True,
        "elapsed": 100,
        "url": "http://www.example.com"
    }

    or

    {
        "name": "foo",
        "success": True,
        "steps": [
            {
                "name": "bar",
                "success": True,
                "elapsed": 100,
                "url": "http://www.example.com"
            }
        ]
    }
    """
    stat_info = {"name": step_data.name}

    # no sub steps
    if isinstance(step_data.data, SessionData):
        stat_info.update(get_session_data_stat(step_data.data))
    # with sub steps
    elif isinstance(step_data.data, list):
        stat_info["success"] = step_data.success
        stat_info["steps"] = [get_step_data_stat(_) for _ in step_data.data]

    return stat_info


def get_testcase_stat(testcase: HttpRunner) -> dict:
    """
    Retrieve stat info from testcase summary.

    >>> get_testcase_stat(...)
    {
        "name": "foo",
        "success": True,
        "fullname": "foo.bar.baz.TestFoo"
        "steps": [
            {
                "name": "foo",
                "success": True,
                "elapsed": 100,
                "url": "http://www.example.com"
            }
        ]
    }
    """
    testcase_summary = testcase.get_summary()
    return {
        "name": testcase_summary.name,
        "success": testcase_summary.success,
        "fullname": f"{type(testcase).__module__}.{type(testcase).__qualname__}",
        "steps": [get_step_data_stat(_) for _ in testcase_summary.step_datas],
    }
