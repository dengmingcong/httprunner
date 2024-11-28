from httprunner.builtin.jsoncomparator.comparator import JSONComparator


class TestAllJSONObjects:
    json_comparator = JSONComparator(False)

    def test_unique_key_usable_and_equal(self):
        result = self.json_comparator.compare_json(
            [{"a": 1}, {"a": 2}, {"a": 3}], [{"a": 3}, {"a": 2}, {"a": 1}]
        )
        assert result.is_success

    def test_value_contains_boolean_and_equal(self):
        result = self.json_comparator.compare_json(
            [{"a": True}, {"a": False}, {"a": 1}, {"a": 0}],
            [{"a": 1}, {"a": 0}, {"a": False}, {"a": True}],
        )
        assert result.is_success

    def test_1p0_equal_1(self):
        result = self.json_comparator.compare_json(
            [{"a": 1.0}, {"a": 2.0}, {"a": 3.0}],
            [{"a": 1}, {"a": 2.0}, {"a": 3}],
        )
        assert result.is_success
