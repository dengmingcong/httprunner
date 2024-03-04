import unittest

import requests

from httprunner.models import JMESPathExtractor, Validator
from httprunner.response import ResponseObject


class TestResponse(unittest.TestCase):
    def setUp(self) -> None:
        resp = requests.post(
            "https://www.postman-echo.com/post",
            json={
                "locations": [
                    {"name": "Seattle", "state": "WA"},
                    {"name": "New York", "state": "NY"},
                    {"name": "Bellevue", "state": "WA"},
                    {"name": "Olympia", "state": "WA"},
                ]
            },
            verify=False,
        )
        self.resp_obj = ResponseObject(resp)

    def test_extract(self):
        extract_mapping = self.resp_obj.extract(
            [
                JMESPathExtractor(
                    variable_name="var_1", expression="body.json.locations[0]"
                ),
                JMESPathExtractor(
                    variable_name="var_2", expression="body.json.locations[3].name"
                ),
            ]
        )
        self.assertEqual(extract_mapping["var_1"], {"name": "Seattle", "state": "WA"})
        self.assertEqual(extract_mapping["var_2"], "Olympia")

    def test_validate(self):
        self.resp_obj.validate(
            [
                Validator(
                    method="equal",
                    expression="body.json.locations[0].name",
                    expect="Seattle",
                ),
                Validator(
                    method="equal",
                    expression="body.json.locations[0]",
                    expect={"name": "Seattle", "state": "WA"},
                ),
            ],
        )

    def test_validate_variables(self):
        variables_mapping = {"index": 1, "var_empty": ""}
        self.resp_obj.validate(
            [
                Validator(
                    method="equal",
                    expression="body.json.locations[$index].name",
                    expect="New York",
                ),
                Validator(method="equal", expression="$var_empty", expect=""),
            ],
            variables_mapping=variables_mapping,
        )

    def test_validate_functions(self):
        variables_mapping = {"index": 1}
        functions_mapping = {"get_num": lambda x: x}
        self.resp_obj.validate(
            [
                Validator(method="equal", expression="${get_num(0)}", expect=0),
                Validator(method="equal", expression="${get_num($index)}", expect=1),
            ],
            variables_mapping=variables_mapping,
            functions_mapping=functions_mapping,
        )
