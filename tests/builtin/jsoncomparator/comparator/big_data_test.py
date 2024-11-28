import requests

from httprunner.builtin.jsoncomparator.comparator import JSONComparator

json_comparator = JSONComparator(False)


def test_big_data():
    response: requests.Response = requests.get(
        "http://192.168.104.47:5050/allure-docker-service/projects/"
        "persistent/reports/latest/data/attachments/a8bb9f39e1e8a31b.json"
    )
    data = response.json()

    result = json_comparator.compare_json(
        data["Assert"]["ExpectValue"], data["Assert"]["ActualValue"]
    )
    assert result.is_success

    # Change ExpectValue to fail the test
    data["Assert"]["ExpectValue"]["dailyPlan"][-1]["mealPlanDetailList"][-1][
        "fatMonoG"
    ] = 0.13
    result = json_comparator.compare_json(
        data["Assert"]["ExpectValue"], data["Assert"]["ActualValue"]
    )
    print(result.fail_messages)
    assert not result.is_success
