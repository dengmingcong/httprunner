from httprunner.builtin.jsoncomparator.comparator import JSONComparator


class TestAllJSONObjects:
    json_comparator = JSONComparator(False)

    def test_unique_key_usable_and_equal(self):
        result = self.json_comparator.compare_json(
            [{"a": 1}, {"a": 2}, {"a": 3}], [{"a": 3}, {"a": 2}, {"a": 1}]
        )
        assert result.is_success

    def test_unique_key_not_usable_for_actual(self):
        result = self.json_comparator.compare_json(
            [{"a": 1}, {"a": 2}, {"a": 3}], [{"a": 3}, {"a": 2}, {"a": 2}]
        )
        print(result.fail_messages)
        assert not result.is_success

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

    def test_unique_key_missing_unexpected_in_actual(self):
        result = self.json_comparator.compare_json(
            [{"a": 1}, {"a": 2}, {"a": 3}], [{"a": 3}, {"a": 2}, {"a": 4}]
        )
        print(result.fail_messages)
        assert not result.is_success

        # boolean value in expected
        result = self.json_comparator.compare_json(
            [{"a": True}, {"a": False}],
            [{"a": 2}, {"a": 3}],
        )
        print(result.fail_messages)
        assert not result.is_success

        # boolean value in actual
        result = self.json_comparator.compare_json(
            [{"a": 1}, {"a": 2}],
            [{"a": True}, {"a": False}],
        )
        print(result.fail_messages)
        assert not result.is_success

        # string value
        result = self.json_comparator.compare_json(
            [{"a": "1"}, {"a": "2"}], [{"a": "3"}, {"a": "4"}]
        )
        print(result.fail_messages)
        assert not result.is_success
