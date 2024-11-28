from httprunner.builtin.jsoncomparator.comparator import JSONComparator


class TestJSONComparatorStrictMode:
    json_comparator = JSONComparator(True)

    def test_compare_json_objects_unexpected_key(self):
        result = self.json_comparator.compare_json(
            {"a": 1, "b": 2}, {"a": 1, "b": 2, "c": 3}
        )
        print(result.fail_messages)
        assert not result.is_success

    def test_compare_json_arrays_order_not_equal(self):
        result = self.json_comparator.compare_json([1, 2, 3], [3, 2, 1])
        print(result.fail_messages)
        assert not result.is_success

    def test_compare_json_arrays_nested_order_not_equal(self):
        result = self.json_comparator.compare_json({"a": [1, 2, 3]}, {"a": [3, 2, 1]})
        print(result.fail_messages)
        assert not result.is_success
