import json
from dataclasses import dataclass

from httprunner.client import HttpSession
from httprunner.json_encoders import AllureJSONAttachmentEncoder
from httprunner.models import StepData


def test_step_data():
    step_data = StepData(export_vars={"session": HttpSession()})
    print(step_data.model_dump_json())


def test_bytes_encoder():
    export_vars = {"foo": "foo", "bar": b"bar"}
    print(json.dumps(export_vars, indent=4, cls=AllureJSONAttachmentEncoder))


def test_class_instance_encoder():
    @dataclass
    class Class:
        name: str

    @dataclass
    class Student:
        name: str
        age: int
        class_: Class

    foo = Student(name="foo", age=10, class_=Class("two"))
    print(json.dumps(foo, indent=4, cls=AllureJSONAttachmentEncoder))
