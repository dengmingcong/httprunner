from httprunner.models import StepData
from httprunner.client import HttpSession


def test_step_data():
    step_data = StepData(
        export_vars={
            "session": HttpSession()
        }
    )
    print(step_data.json())
