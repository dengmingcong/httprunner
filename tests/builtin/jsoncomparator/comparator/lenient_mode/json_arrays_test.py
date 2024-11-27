from httprunner.builtin.jsoncomparator.comparator import JSONComparator


class TestCompareJSONArrays:
    json_comparator = JSONComparator(False)

    def test_equal(self):
        result = self.json_comparator.compare_json([1, 2, 3], [1, 2, 3])
        assert result.is_success

    def test_length_not_equal(self):
        result = self.json_comparator.compare_json([1, 2, 3], [1, 2])
        print(result.fail_messages)
        assert not result.is_success

    def test_nested_length_not_equal(self):
        result = self.json_comparator.compare_json({"a": [1, 2, 3]}, {"a": [1, 2]})
        print(result.fail_messages)
        assert not result.is_success

    def test_both_empty(self):
        result = self.json_comparator.compare_json([], [])
        assert result.is_success

    def test_simple_values_equal(self):
        result = self.json_comparator.compare_json(
            {"a": [None, 1, 2.5, "abc", True]},
            {"a": [2.5, None, "abc", True, 1]},
        )
        print(result.fail_messages)
        assert result.is_success

    def test_simple_value_1p0_equal_1(self):
        result = self.json_comparator.compare_json(
            {"a": [1.0, 2.0, 3.0]},
            {"a": [1, 2.0, 3]},
        )
        assert result.is_success

    def test_missing_item(self):
        result = self.json_comparator.compare_json({"a": [1, 2, 3]}, {"a": [1, 2, 2]})
        print(result.fail_messages)
        assert not result.is_success

    def test_unexpected_item(self):
        result = self.json_comparator.compare_json(
            {"a": [1, 2, 3, 3]}, {"a": [1, 2, 3, 4]}
        )
        print(result.fail_messages)
        assert not result.is_success
