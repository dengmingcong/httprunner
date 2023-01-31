import json


class ExportVariableEncoder(json.JSONEncoder):
    """
    JSON encoder for export vars.
    """

    def default(self, obj):
        if isinstance(obj, bytes):
            return repr(obj)
        return json.JSONEncoder.default(self, obj)
