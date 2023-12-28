import json
from typing import NoReturn

import allure

from httprunner.json_encoders import (
    AllureJSONAttachmentEncoder,
)


def save_extract_export_vars(
    extract_mapping: dict,
    exported_vars: dict,
    is_export_extract_same: bool,
) -> NoReturn:
    """Save export variables to allure report."""
    # display export only if it is the same as extract
    if is_export_extract_same:
        variables = exported_vars
        title = "export"
    # display extract and export separately if they are not the same
    else:
        variables = {
            "extract": extract_mapping,
            "export": exported_vars,
        }
        title = "extract / export"

    allure.attach(
        json.dumps(
            variables,
            indent=4,
            ensure_ascii=False,
            cls=AllureJSONAttachmentEncoder,
        ),
        title,
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
