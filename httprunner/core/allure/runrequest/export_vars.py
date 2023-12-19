import json
from typing import NoReturn

import allure

from httprunner.json_encoders import (
    AllureJSONAttachmentEncoder,
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
        "exported variables",
        allure.attachment_type.JSON,
    )
