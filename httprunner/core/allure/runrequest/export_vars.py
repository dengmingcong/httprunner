import json
from typing import NoReturn

import allure

from httprunner.json_encoders import (
    AllureJSONAttachmentEncoder,
)


def save_extract_export_vars(
    extract_mapping: dict,
    exported_vars: dict,
) -> NoReturn:
    """Save export variables to allure report."""
    allure.attach(
        json.dumps(
            extract_mapping,
            indent=4,
            ensure_ascii=False,
            cls=AllureJSONAttachmentEncoder,
        ),
        "extract",
        allure.attachment_type.JSON,
    )
    allure.attach(
        json.dumps(
            exported_vars,
            indent=4,
            ensure_ascii=False,
            cls=AllureJSONAttachmentEncoder,
        ),
        "export",
        allure.attachment_type.JSON,
    )


def save_export_vars(
    exported_vars: dict,
) -> NoReturn:
    """Save export variables to allure report."""
    allure.attach(
        json.dumps(
            exported_vars,
            indent=4,
            ensure_ascii=False,
            cls=AllureJSONAttachmentEncoder,
        ),
        "export",
        allure.attachment_type.JSON,
    )
