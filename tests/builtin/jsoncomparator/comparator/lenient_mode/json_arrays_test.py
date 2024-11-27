from httprunner.builtin.jsoncomparator.comparator import JSONComparator


class TestCompareJSONArrays:
    json_comparator = JSONComparator(False)

    def test_compare_json_arrays_equal(self):
        result = self.json_comparator.compare_json([1, 2, 3], [1, 2, 3])
        assert result.is_success

    def test_compare_json_arrays_length_not_equal(self):
        result = self.json_comparator.compare_json([1, 2, 3], [1, 2])
        print(result.fail_messages)
        assert not result.is_success

    def test_compare_json_arrays_nested_length_not_equal(self):
        result = self.json_comparator.compare_json({"a": [1, 2, 3]}, {"a": [1, 2]})
        print(result.fail_messages)
        assert not result.is_success

    def test_compare_json_arrays_both_empty(self):
        result = self.json_comparator.compare_json([], [])
        assert result.is_success

    def test_compare_json_arrays_simple_values_equal(self):
        result = self.json_comparator.compare_json(
            {"a": [None, 1, 2.5, "abc", True, None]},
            {"a": [2.5, None, "abc", None, 1, 1]},
        )
        print(result.fail_messages)

    def test_compare_json_arrays_missing_item(self):
        result = self.json_comparator.compare_json({"a": [1, 2, 3]}, {"a": [1, 2, 2]})
        print(result.fail_messages)
        assert not result.is_success

    def test_compare_json_arrays_unexpected_item(self):
        result = self.json_comparator.compare_json(
            {"a": [1, 2, 3, 3]}, {"a": [1, 2, 3, 4]}
        )
        print(result.fail_messages)
        assert not result.is_success
