import json

from pydantic import BaseModel
from pydantic_core import PydanticSerializationError


def pydantic_model_dump_json(model: BaseModel, **kwargs) -> str:
    """Fallback to built-in `json.dumps` when error occurred while executing BaseModel.model_dump_json()."""
    if not isinstance(model, BaseModel):
        raise TypeError("argument model must be an instance of pydantic BaseModel.")

    try:
        return model.model_dump_json(**kwargs)
    except PydanticSerializationError:
        return json.dumps(
            model.model_dump(),
            indent=4,
            ensure_ascii=False,
            cls=AllureJSONAttachmentEncoder,
        )


class AllureJSONAttachmentEncoder(json.JSONEncoder):
    """
    JSON encoder for saving allure attachments.

    Note:
        According to the official documentation,
        > "If specified, default should be a function that gets called for objects that can’t otherwise be serialized."
        function default would not be called if objects can be serialized.
    """

    def default(self, o):
        # bytes
        return repr(o)
