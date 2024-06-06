"""Record and track the comparison results of JSONs."""

from typing import Any


class FailField:
    """Models a field failure when comparing values from both the expected and actual JSONs."""

    def __init__(self, field_path, expected, actual):
        """Init a object.

        :param field_path: path to the field that is currently being compared.
        :param expected: expected value of the field. \
            When one key is missing in actual JSON object, the value is the missing key, \
            when an item is missing in actual JSON array, the value is the missing item. \
        :param actual: actual value of the field. \
            In STRICT mode, when one key exists in actual JSON object unexpectedly, the value is the unexpected key.
        """
        self.field_path = field_path
        self.expected = expected
        self.actual = actual


class JSONCompareResult:
    """Hold the results from JSONComparator.

    It identifies the entire JSON comparison result, not one specific field.

    Attributes:
        - is_success: whether the comparison passed, it identifies the entire JSON comparison result, not one field
        - fail_messages: messages of all failed fields
        - current_field_path: path to the field that is currently being compared
        - current_field_expected: expected value of the field that is currently being compared
        - current_field_actual: actual value of the field that is currently being compared
        - mismatch_fields: filed path exists both in expected and actual JSONs, but with mismatched values
        - missing_fields: filed path exists in expected JSON but not in actual JSON
        - unexpected_fields: field path exists in actual JSON but not in expected JSON
    """

    def __init__(self, is_success: bool = True, fail_messages: str = ""):
        """Init the JSONCompareResult.

        :param is_success: whether the comparison passed, it identifies the entire JSON comparison result, not one field
        :param fail_messages: messages of all mismatched fields
        """
        self.is_success = is_success
        self.fail_messages = fail_messages
        self.current_field_path = None  # TODO: decide if this is needed
        self.current_field_expected = None
        self.current_field_actual = None
        self.mismatch_fields: list[FailField] = []
        self.missing_fields: list[FailField] = []
        self.unexpected_fields: list[FailField] = []

    def fail(self, message: str) -> "JSONCompareResult":
        """Fail the entire JSON comparison and add fail message."""
        # fail the entire JSON comparison
        self.is_success = False

        # add fail message, separated by ";"
        self.fail_messages += " ; " + message

        return self

    @staticmethod
    def describe(field_value: Any) -> str:
        """Describe the field value in a human-readable way.

        :param field_value: the value of the field, either expected or actual
        :return: a human-readable string representation of the field value
        """
        if isinstance(field_value, dict):
            return "a JSON object"

        if isinstance(field_value, list):
            return "a JSON array"

        return repr(field_value)

    def add_mismatch_field(
        self, field_path: str, expected: Any, actual: Any
    ) -> "JSONCompareResult":
        """Add a mismatched field.

        Mismatched fields are fields that exist both in expected and actual JSONs, but with mismatched values.
        """
        # append this field to the mismatched fields list
        self.mismatch_fields.append(FailField(field_path, expected, actual))

        # change the current field cursor
        self.current_field_path = field_path
        self.current_field_expected = expected
        self.current_field_actual = actual

        # fail the entire JSON comparison
        self.fail(
            f"{field_path}\n    expected: {self.describe(expected)}\n    got: {self.describe(actual)}\n"
        )

        return self

    def add_missing_field(self, field_path: str, expected: Any) -> "JSONCompareResult":
        """Add a missing field.

        :param field_path: path to the field that is currently being compared
        :param expected: an object key or array item that is missing in actual JSON. \
            when comparing two JSON objects, it's the key that exists in the expected object but not in actual object, \
            when comparing two JSON arrays, it's the item that exists in the expected array but not in actual array.
        """
        # append this field to the missing fields list
        self.missing_fields.append(FailField(field_path, expected, None))

        # change the current field cursor
        self.current_field_path = field_path
        self.current_field_expected = expected
        self.current_field_actual = None

        # fail the entire JSON comparison
        self.fail(
            f"{field_path}\n    expected: {self.describe(expected)}\n    but none found\n"
        )

        return self

    def add_unexpected_field(self, field_path: str, actual: Any) -> "JSONCompareResult":
        """Add an unexpected field.

        :param field_path: path to the field that is currently being compared
        :param actual: an object key or array item that is unexpected in actual JSON. \
            when comparing two JSON objects, it's the key that exists in the actual object but not in expected object, \
            when comparing two JSON arrays, it's the item that exists in the actual array but not in expected array.
        """
        # append this field to the unexpected fields list
        self.unexpected_fields.append(FailField(field_path, None, actual))

        # change the current field cursor
        self.current_field_path = field_path
        self.current_field_actual = actual
        self.current_field_expected = None

        # fail the entire JSON comparison
        self.fail(f"{field_path}\n    unexpected: {self.describe(actual)}\n")

        return self
