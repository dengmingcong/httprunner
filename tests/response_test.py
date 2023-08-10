import unittest

import requests

from httprunner.models import JMESPathExtractor
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
                {"eq": ["body.json.locations[0].name", "Seattle"]},
                {"eq": ["body.json.locations[0]", {"name": "Seattle", "state": "WA"}]},
            ],
        )

    def test_validate_variables(self):
        variables_mapping = {"index": 1, "var_empty": ""}
        self.resp_obj.validate(
            [
                {"eq": ["body.json.locations[$index].name", "New York"]},
                {"eq": ["$var_empty", ""]},
            ],
            variables_mapping=variables_mapping,
        )

    def test_validate_functions(self):
        variables_mapping = {"index": 1}
        functions_mapping = {"get_num": lambda x: x}
        self.resp_obj.validate(
            [
                {"eq": ["${get_num(0)}", 0]},
                {"eq": ["${get_num($index)}", 1]},
            ],
            variables_mapping=variables_mapping,
            functions_mapping=functions_mapping,
        )
