import json

import allure

from httprunner.configs.validation import validation_settings
from httprunner.json_encoders import AllureJSONAttachmentEncoder
from httprunner.response import ResponseObject


def save_validation_result(
    response_obj: ResponseObject,
) -> None:
    """Save validation result to allure report."""
    validation_result: dict
    for validation_result in response_obj.validation_results.get(
        "validate_extractor", []
    ):
        jmespath_ = validation_result.get(validation_settings.content.keys.jmespath_)
        # it is possible that jmespath is not str
        jmespath_ = jmespath_ if isinstance(jmespath_, str) else "NA"

        result = validation_result.pop(validation_settings.content.keys.result, "NA")
        comparator = validation_result.get(
            validation_settings.content.keys.assert_, {}
        ).get(validation_settings.content.keys.comparator, "NA")

        validation_attachment_name = f"{result} validate - {jmespath_} / {comparator}"

        allure.attach(
            json.dumps(
                validation_result,
                indent=4,
                ensure_ascii=False,
                cls=AllureJSONAttachmentEncoder,
            ),
            validation_attachment_name,
            allure.attachment_type.JSON,
        )
