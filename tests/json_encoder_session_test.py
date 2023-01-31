import json

from httprunner.client import HttpSession
from httprunner.json_encoders import ExportVariableEncoder
from httprunner.models import StepData


def test_step_data():
    step_data = StepData(export_vars={"session": HttpSession()})
    print(step_data.json())


def test_bytes_encoder():
    export_vars = {"foo": "foo", "bar": b"bar"}
    print(json.dumps(export_vars, indent=4, cls=ExportVariableEncoder))
