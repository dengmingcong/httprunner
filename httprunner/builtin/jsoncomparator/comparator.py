"""Main module for JSON comparator."""

from typing import Any, Union

from httprunner.builtin.jsoncomparator import util as jsoncomparator_util
from httprunner.builtin.jsoncomparator.result import JSONCompareResult


class JSONComparator:
    """Main class for JSON comparator."""

    def __init__(self, is_strict: bool = False) -> None:
        """Init the JSONComparator.

        ref: https://github.com/skyscreamer/JSONassert

        :param is_strict: whether to compare with strict mode, default is False. \
            The original JSON comparison logic has four modes: STRICT, LENIENT, NON_EXTENSIBLE, STRICT_ORDER, \
            but we only implement two of them: STRICT and LENIENT. \
            If is_strict is True, then compare with STRICT mode, otherwise compare with LENIENT mode.
        """
        self.is_strict = is_strict

    def _compare_field_values(
        self, prefix: str, expected: Any, actual: Any, result: JSONCompareResult
    ):
        """Compare the expected field value with the actual field value.

        :param prefix: field path prefix.
        :param expected: the expected field value.
        :param actual: the actual field value.
        :param result: JSONCompareResult instance.
        """
        # Return directly if expected and actual are the same.
        if expected == actual:
            return

        # One is None and the other is not None, this field is a mismatched field.
        if (expected is None and actual is not None) or (
            expected is not None and actual is None
        ):
            result.add_mismatch_field(prefix, expected, actual)
            return

        # Note: In Python, 1.0 and 1 has different types, but they are equal (assert 1.0 == 1),
        # so we cannot compare their types here.
        # Both are simple values, compare them directly.
        if jsoncomparator_util.is_simple_value(
            expected
        ) and jsoncomparator_util.is_simple_value(actual):
            if expected != actual:
                result.add_mismatch_field(prefix, expected, actual)
            return

        # Both are JSON objects, call compare_json_objects.
        if isinstance(expected, dict) and isinstance(actual, dict):
            self._compare_json_objects(prefix, expected, actual, result)
            return

        # Both are JSON arrays, call compare_json_arrays.
        if isinstance(expected, list) and isinstance(actual, list):
            self._compare_json_arrays(prefix, expected, actual, result)
            return

        # Valid JSON types contains:
        # number (int, float), string (str), boolean (bool), array (list), object (dict), null (None),
        # all other types are invalid JSON types.
        result.add_mismatch_field(prefix, expected, actual)

    def _check_expected_json_object_keys_in_actual(
        self, prefix: str, expected: dict, actual: dict, result: JSONCompareResult
    ):
        """Check keys of expected JSON object are all in actual JSON object.

        :param prefix: field path prefix.
        :param expected: expected JSON object.
        :param actual: actual JSON object.
        :param result: a JSONCompareResult instance.
        """
        for expected_object_key, expected_object_value in expected.items():
            if expected_object_key in actual:
                # Key exists both in expected and actual, need to compare field values.
                self._compare_field_values(
                    f"{prefix}.{expected_object_key}",
                    expected_object_value,
                    actual[expected_object_key],
                    result,
                )
            else:
                # Keys that exist in expected but not in actual are missing fields.
                result.add_missing_field(prefix, expected_object_key)

    def _check_actual_json_object_keys_in_expected(
        self, prefix: str, expected: dict, actual: dict, result: JSONCompareResult
    ):
        """Check keys of actual JSON object are all in expected JSON object.

        Call this method only when is_strict is True.

        :param prefix: field path prefix.
        :param expected: expected JSON object.
        :param actual: actual JSON object.
        :param result: a JSONCompareResult instance.
        """
        # In STRICT mode, keys that exist in actual but not in expected are unexpected fields.
        for key in set(actual.keys()) - set(expected.keys()):
            result.add_unexpected_field(prefix, key)

    def _compare_json_objects(
        self, prefix: str, expected: dict, actual: dict, result: JSONCompareResult
    ):
        """Compare two JSON objects.

        :param prefix: field path prefix.
        :param expected: expected JSON object.
        :param actual: actual JSON object.
        :param result: a JSONCompareResult instance.
        """
        # Check that every key of expected JSON object is in actual JSON object.
        self._check_expected_json_object_keys_in_actual(
            prefix, expected, actual, result
        )

        # If is_strict is True, check that every key of actual JSON object is in expected JSON object.
        if self.is_strict:
            self._check_actual_json_object_keys_in_expected(
                prefix, expected, actual, result
            )

    def _compare_json_arrays_with_strict_order(
        self, prefix: str, expected: list, actual: list, result: JSONCompareResult
    ):
        """Compare two JSON arrays with strict order.

        The values in the same index should match.

        :param prefix: field path prefix.
        :param expected: expected JSON array.
        :param actual: actual JSON array.
        :param result: a JSONCompareResult instance.
        """
        for expected_array_index, expected_array_value in enumerate(expected):
            self._compare_field_values(
                f"{prefix}[{expected_array_index}]",
                expected_array_value,
                actual[expected_array_index],
                result,
            )

    def _compare_json_arrays_all_simple_values(
        self, prefix: str, expected: list, actual: list, result: JSONCompareResult
    ):
        """Compare two JSON arrays with all values being simple values.

        The comparison is done in non strict mode, so the order of the values does not matter.

        :param prefix: field path prefix.
        :param expected: expected JSON array.
        :param actual: actual JSON array.
        :param result: a JSONCompareResult instance.
        """
        expected_item_to_count_mapping = jsoncomparator_util.get_cardinality_mapping(
            expected
        )
        actual_item_to_count_mapping = jsoncomparator_util.get_cardinality_mapping(
            actual
        )

        # Iterate over the expected mapping to find missing and mismatched items.
        for expected_item, expected_count in expected_item_to_count_mapping.items():
            # If the expected item is not in the actual mapping, this item is a missing item.
            if expected_item not in actual_item_to_count_mapping:
                result.add_missing_field(f"{prefix}[]", expected_item)
            # If the expected count is different from the actual count, this value is a mismatched item.
            elif expected_count != (
                actual_count := actual_item_to_count_mapping[expected_item]
            ):
                result.fail(
                    f"{prefix}[]: Expected {expected_count} occurrence(s) of {expected_item} "
                    f"but got {actual_count} occurrence(s)"
                )

        # Iterate over the actual mapping to find unexpected items.
        for actual_item in actual_item_to_count_mapping:
            if actual_item not in expected_item_to_count_mapping:
                result.add_unexpected_field(f"{prefix}[]", actual_item)

    def _compare_json_arrays_all_json_objects(
        self, prefix: str, expected: list, actual: list, result: JSONCompareResult
    ):
        """Compare two JSON arrays with all values being JSON objects.

        :param prefix: the field path prefix.
        :param expected: expected JSON array.
        :param actual: actual JSON array.
        :param result: a JSONCompareResult instance.
        """
        unique_key = jsoncomparator_util.find_unique_key(expected)

        # If no unique key found from expected or the unique key was not unique in actual JSON array,
        # we have to compare them with an expensive way.
        if not unique_key or not jsoncomparator_util.is_usable_as_unique_key(
            unique_key, actual
        ):
            self._compare_json_arrays_recursively(prefix, expected, actual, result)
            return

        # If a unique key was found, convert the JSON arrays to dictionaries and compare them.
        expected_mapping = jsoncomparator_util.convert_array_of_json_objects_to_mapping(
            expected, unique_key
        )
        actual_mapping = jsoncomparator_util.convert_array_of_json_objects_to_mapping(
            actual, unique_key
        )

        # Iterate over the expected mapping to find missing and mismatched items.
        for unique_key_value, expected_json_object in expected_mapping.items():
            # If any value of the unique key is not in the actual mapping, this item is a missing item.
            if unique_key_value not in actual_mapping:
                result.add_missing_field(
                    jsoncomparator_util.format_unique_key(
                        prefix, unique_key, unique_key_value
                    ),
                    expected_json_object,
                )
                continue

            # If the unique key value is in the actual mapping, compare the two JSON objects.
            self._compare_field_values(
                jsoncomparator_util.format_unique_key(
                    prefix, unique_key, unique_key_value
                ),
                expected_json_object,
                actual_mapping[unique_key_value],
                result,
            )

        # Iterate over the actual mapping to find unexpected items.
        for unique_key_value, actual_json_object in actual_mapping:
            if unique_key_value not in expected_mapping:
                result.add_unexpected_field(
                    jsoncomparator_util.format_unique_key(
                        prefix, unique_key, unique_key_value
                    ),
                    actual_json_object,
                )

    def _compare_json_arrays_recursively(
        self, prefix: str, expected: list, actual: list, result: JSONCompareResult
    ):
        """Compare two JSON arrays recursively.

        This is expensive (O(n^2)), but may be the only resort for some cases with loose array ordering, and no
        easy way to uniquely identify each element.

        :param prefix: field path prefix.
        :param expected: expected JSON array.
        :param actual: actual JSON array.
        :param result: a JSONCompareResult instance.
        """
        # If one item of actual array matches one in the expected array,
        # it's index in actual array will be added to the matched_indexes set.
        matched_indexes = set()

        # Iterate over the expected array in outer loop.
        for expected_index, expected_item in enumerate(expected):
            # Set initial value of match_found to False,
            # when a match was found in the inner (actual) loop, set it to True,
            # if no match was found in the inner (actual) loop, fail the comparison.
            match_found = False

            # Iterate over the actual array in inner loop.
            for actual_index, actual_item in enumerate(actual):
                # If one item is None and the other is not None, continue to the next iteration.
                if (expected_item is None and actual_item is not None) or (
                    expected_item is not None and actual_item is None
                ):
                    continue

                # Skip the item if it has been matched.
                if actual_index in matched_indexes:
                    continue

                # Continue if the data type of the two items are different.
                # Note: When comparing items of arrays, the data type must be the same,
                # this behavior is different from comparing objects,
                # but is consistent with method _compare_json_arrays_all_simple_values().
                if type(expected_item) is not type(actual_item):
                    continue

                # The actual item should have the same data type as the expected item,
                # because data type has been checked above.
                # Call compare_json() if the the expected item is a JSON object or a JSON array.
                if isinstance(expected_item, (dict, list)):
                    # If the comparison is successful, add the actual index to the matched_indexes set.
                    if self.compare_json(expected_item, actual_item).is_success:
                        matched_indexes.add(actual_index)
                        match_found = True
                        break
                # If the expected item is a simple value, compare them directly.
                elif expected_item == actual_item:
                    matched_indexes.add(actual_index)
                    match_found = True
                    break

            # If no match is found in the inner (actual) loop, fail the comparison.
            if not match_found:
                result.fail(
                    f"{prefix}[{expected_index}] Could not find match for element {expected_item}"
                )

                return

    def _compare_json_arrays(
        self, prefix: str, expected: list, actual: list, result: JSONCompareResult
    ):
        """Compare two JSON arrays.

        :param prefix: field path prefix.
        :param expected: expected JSON array.
        :param actual: actual JSON array.
        :param result: a JSONCompareResult instance.
        """
        # Compare the length of the two arrays.
        # Fail the comparison if the lengths are different.
        if len(expected) != len(actual):
            result.fail(
                f"{prefix}[]: Expected {len(expected)} values but got {len(actual)}"
            )
            return
        # Return directly if the two arrays are empty.
        elif not expected:
            return

        # If is_strict is True, compare the two arrays with strict order.
        if self.is_strict:
            self._compare_json_arrays_with_strict_order(
                prefix, expected, actual, result
            )

        # The other cases, compare the two arrays in non strict mode.
        # If all values in the expected array are simple values, compare them in non strict mode.
        elif jsoncomparator_util.is_all_simple_values_array(expected):
            self._compare_json_arrays_all_simple_values(
                prefix, expected, actual, result
            )
        # If all values in the expected array are JSON objects, call _compare_json_arrays_all_json_objects().
        elif jsoncomparator_util.is_all_json_objects_array(expected):
            self._compare_json_arrays_all_json_objects(prefix, expected, actual, result)
        # Otherwise, call _compare_json_arrays_recursively().
        else:
            self._compare_json_arrays_recursively(prefix, expected, actual, result)

    def compare_json(
        self,
        expected: Union[dict, list],
        actual: Union[dict, list],
    ) -> JSONCompareResult:
        """Compare two JSONs (JSON object or JSON array)."""
        result = JSONCompareResult()

        # If both expected and actual are JSON objects, call _compare_json_objects().
        if isinstance(expected, dict) and isinstance(actual, dict):
            self._compare_json_objects("", expected, actual, result)
        # If both expected and actual are JSON arrays, call compare_json_arrays.
        elif isinstance(expected, list) and isinstance(actual, list):
            self._compare_json_arrays("", expected, actual, result)
        # Otherwise, add a mismatched field.
        else:
            result.add_mismatch_field("", expected, actual)

        return result
