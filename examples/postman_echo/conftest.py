# NOTICE: Generated By HttpRunner.
import json
import os
import time

import pytest
from loguru import logger

from httprunner.statistics import get_testcase_stat
from httprunner.utils import get_platform, ExtendJSONEncoder


def pytest_addoption(parser):
    parser.addoption(
        "--stat-file", action="store", help="file to store statistics data"
    )


@pytest.fixture(scope="session", autouse=True)
def save_stat_data(request):
    """Save stat data."""
    yield

    if stat_file := request.config.getoption("--stat-file"):
        if not os.path.isabs(stat_file):
            stat_file = os.path.join(os.getcwd(), stat_file)
        stat_dir = os.path.dirname(stat_file)
        os.makedirs(stat_dir, exist_ok=True)

        logger.info("task finished, collect statistics for option --stat-file")

        stat_info = [get_testcase_stat(item.instance) for item in request.node.items]

        with open(stat_file, "w", encoding="utf-8") as f:
            json.dump(stat_info, f, indent=4, ensure_ascii=False, cls=ExtendJSONEncoder)

        logger.info(f"generate stat file: {stat_file}")


@pytest.fixture(scope="session", autouse=True)
def session_fixture(request):
    """setup and teardown each task"""
    logger.info("start running testcases ...")

    start_at = time.time()

    yield

    logger.info("task finished, generate task summary for --save-tests")

    summary = {
        "success": True,
        "stat": {
            "testcases": {"total": 0, "success": 0, "fail": 0},
            "teststeps": {"total": 0, "failures": 0, "successes": 0},
        },
        "time": {"start_at": start_at, "duration": time.time() - start_at},
        "platform": get_platform(),
        "details": [],
    }

    for item in request.node.items:
        testcase_summary = item.instance.get_summary()
        summary["success"] &= testcase_summary.success

        summary["stat"]["testcases"]["total"] += 1
        summary["stat"]["teststeps"]["total"] += len(testcase_summary.step_datas)
        if testcase_summary.success:
            summary["stat"]["testcases"]["success"] += 1
            summary["stat"]["teststeps"]["successes"] += len(
                testcase_summary.step_datas
            )
        else:
            summary["stat"]["testcases"]["fail"] += 1
            summary["stat"]["teststeps"]["successes"] += (
                len(testcase_summary.step_datas) - 1
            )
            summary["stat"]["teststeps"]["failures"] += 1

        testcase_summary_json = testcase_summary.dict()
        testcase_summary_json["records"] = testcase_summary_json.pop("step_datas")
        summary["details"].append(testcase_summary_json)

    summary_path = (
        "/Users/debugtalk/MyProjects/HttpRunner-dev/HttpRunner/"
        "examples/postman_echo/logs/request_methods/hardcode.summary.json"
    )
    summary_dir = os.path.dirname(summary_path)
    os.makedirs(summary_dir, exist_ok=True)

    with open(summary_path, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=4, ensure_ascii=False, cls=ExtendJSONEncoder)

    logger.info(f"generated task summary: {summary_path}")


@pytest.fixture(scope="function", autouse=True)
def clean_session_variables(request):
    """setup and teardown each testcase"""
    request.instance.with_variables({})
