# NOTE: Generated By HttpRunner v3.1.4
# FROM: request_methods/request_with_testcase_reference.yml


import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))


from httprunner import HttpRunner, Config, Step, RunRequest, RunTestCase
from httprunner.exceptions import ParamsError, VariableNotFound

from .base_request import (
    TestCaseRequestAndExport as RequestAndExport,
)


@pytest.mark.xfail(raises=ParamsError)
class TestFailToExportIfValueInVarNames(HttpRunner):

    config = (
        Config("request methods testcase: reference testcase and export alias")
        .base_url("https://postman-echo.com")
        .verify(False)
    )

    teststeps = [
        Step(
            RunTestCase("type of value is not str")
            .call(RequestAndExport)
            .export("v02", v01="v02")
        ),
    ]


class TestExportKeyEqualsValue(HttpRunner):

    config = (
        Config("request methods testcase: reference testcase and export alias")
        .base_url("https://postman-echo.com")
        .verify(False)
    )

    teststeps = [
        Step(
            RunTestCase("export: key equals value")
            .call(RequestAndExport)
            .export(v01="v01")
        ),
        Step(
            RunRequest("post form data")
            .post("/post")
            .with_json(
                {
                    "key01": "$v01",
                }
            )
            .validate()
            .assert_equal("status_code", 200)
            .assert_equal("body.json.key01", 1)
        ),
    ]


@pytest.mark.xfail(raises=VariableNotFound)
class TestFailToExportWhenVariableNotFound(HttpRunner):

    config = (
        Config("request methods testcase: reference testcase and export alias")
        .base_url("https://postman-echo.com")
        .verify(False)
    )

    teststeps = [
        Step(
            RunTestCase("type of value is not str")
            .call(RequestAndExport)
            .export("v06", v07="v007")
        ),
    ]


class TestExportIntersectionSet(HttpRunner):

    config = (
        Config("request methods testcase: reference testcase and export alias")
        .base_url("https://postman-echo.com")
        .verify(False)
    )

    teststeps = [
        Step(
            RunTestCase("export: intersection set")
            .call(RequestAndExport)
            .export("v01", v01="v001")
        ),
        Step(
            RunRequest("post form data")
            .post("/post")
            .with_json(
                {
                    "key01": "$v01",
                    "key02": "$v001",
                }
            )
            .validate()
            .assert_equal("status_code", 200)
            .assert_equal("body.json.key01", 1)
            .assert_equal("body.json.key02", 1)
        ),
    ]


class TestExportVarNamesOnly(HttpRunner):

    config = (
        Config("request methods testcase: reference testcase and export alias")
        .base_url("https://postman-echo.com")
        .verify(False)
    )

    teststeps = [
        Step(
            RunTestCase("export var names only")
            .call(RequestAndExport)
            .export(*["v01", "v02", "v03", "v04", "v"])
        ),
        Step(
            RunRequest("post form data")
            .post("/post")
            .with_json(
                {
                    "key01": "$v01",
                    "key02": "$v02",
                    "key03": "$v03",
                    "key04": "$v04",
                    "key05": "$v",
                }
            )
            .validate()
            .assert_equal("status_code", 200)
            .assert_equal("body.json.key01", 1)
            .assert_equal("body.json.key02", "value02")
            .assert_equal("body.json.key03", [1, 2, 3])
            .assert_equal("body.json.key04", {"foo": "bar"})
            .assert_equal("body.json.key05", "value")
        ),
    ]


class TestExportOnlyInAliasMapping(HttpRunner):

    config = (
        Config("request methods testcase: reference testcase and export alias")
        .base_url("https://postman-echo.com")
        .verify(False)
    )

    teststeps = [
        Step(
            RunTestCase("export: alias mapping only")
            .call(RequestAndExport)
            .export(v01="v001", v02="v002")
        ),
        Step(
            RunRequest("post form data")
            .post("/post")
            .with_json(
                {
                    "key01": "$v001",
                    "key02": "$v002",
                }
            )
            .validate()
            .assert_equal("status_code", 200)
            .assert_equal("body.json.key01", 1)
            .assert_equal("body.json.key02", "value02")
        ),
    ]


class TestExportOnlyInAliasMappingAndReference(HttpRunner):

    config = (
        Config("request methods testcase: reference testcase and export alias")
        .base_url("https://postman-echo.com")
        .verify(False)
    )

    teststeps = [
        Step(
            RunTestCase("export: alias mapping only")
            .call(RequestAndExport)
            .export(v01="v001")
        ),
        Step(
            RunRequest("post form data")
            .post("/post")
            .with_json(
                {
                    "key01": "$v01",
                    "key02": "$v001",
                }
            )
            .validate()
            .assert_equal("status_code", 200)
            .assert_equal("body.json.key01", 1)
            .assert_equal("body.json.key02", 1)
        ),
    ]
