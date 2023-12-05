import json

from pydantic_core import PydanticSerializationError


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
        if isinstance(o, bytes):
            return repr(o)

        # functions
        if callable(o):
            return repr(o)

        try:
            return json.JSONEncoder.default(self, o)
        except (PydanticSerializationError, json.JSONDecodeError, TypeError):
            return repr(o)
