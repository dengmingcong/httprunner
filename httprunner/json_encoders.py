import json


class ExportVariableEncoder(json.JSONEncoder):
    """
    JSON encoder for export vars.
    """

    def default(self, o):
        # bytes
        if isinstance(o, bytes):
            return repr(o)

        # has attribute __dict__
        if hasattr(o, "__dict__"):
            return o.__dict__

        return json.JSONEncoder.default(self, o)
