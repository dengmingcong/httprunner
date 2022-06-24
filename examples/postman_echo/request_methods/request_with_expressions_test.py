from pydantic import BaseModel

from httprunner import HttpRunner, Config, Step, RunRequest


class Obj(BaseModel):
    foo: list = [{}, {"bar": [1, 2, 3]}]


class TestCaseRequestWithExpressions(HttpRunner):

    config = (
        Config("request methods testcase with expressions")
        .variables(**{"foo1": "config_bar1", "foo2": "config_bar2", "obj": Obj()})
        .base_url("https://postman-echo.com")
        .verify(False)
    )

    teststeps = [
        Step(
            RunRequest("get with params")
            .with_variables(**{"baz": "${obj.foo[1]['$name'][1:2]}", "name": "bar"})
            .post("/post")
            .with_headers(**{"User-Agent": "HttpRunner/${get_httprunner_version()}"})
            .with_json({"foo": "$foo1", "baz": "$baz", "bar": "$foo2"})
            .validate()
            .assert_equal("status_code", 200)
            .assert_equal("body.data.foo", "config_bar1")
            .assert_equal("body.data.baz", [2])
            .assert_equal("body.data.bar", "config_bar2")
        ),
    ]
