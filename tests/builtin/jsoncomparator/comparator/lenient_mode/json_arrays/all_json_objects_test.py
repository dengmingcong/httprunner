from dotwiz import DotWiz

from httprunner.builtin.jsoncomparator.comparator import JSONComparator


class TestAllJSONObjects:
    json_comparator = JSONComparator(False)

    def test_unique_key_usable_and_equal(self):
        result = self.json_comparator.compare_json(
            [{"a": 1}, {"a": 2}, {"a": 3}], [{"a": 3}, {"a": 2}, {"a": 1}]
        )
        assert result.is_success

        # Extra keys in actual.
        result = self.json_comparator.compare_json(
            [{"a": 1}, {"a": 2}, {"a": 3}],
            [{"a": 3, "b": 3}, {"a": 2, "b": 2}, {"a": 1, "b": 1}],
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

    def test_unique_key_value_equal_but_json_not_equal(self):
        result = self.json_comparator.compare_json(
            [{"a": True, "b": 1}, {"a": 2, "b": True}, {"a": 3, "b": "3"}],
            [{"a": True, "b": False}, {"a": 2, "b": 4}, {"a": 3, "b": "4"}],
        )
        print(result.fail_messages)
        assert not result.is_success

    def test_dotwiz(self):
        result = self.json_comparator.compare_json(
            [DotWiz({"a": 1}), {"a": 2}],
            [DotWiz({"a": 1}), DotWiz({"a": 2})],
        )
        assert result.is_success

        # Some keys are DotWiz.
        result = self.json_comparator.compare_json(
            [{"a": DotWiz({"b": 1}), "c": 1}, {"a": 2}],
            [{"a": {"b": 1}, "c": 1}, DotWiz({"a": 2})],
        )
        assert result.is_success

        # Unique key is usable.
        result = self.json_comparator.compare_json(
            [DotWiz({"a": 1}), DotWiz({"a": 2}), DotWiz({"a": 3})],
            [{"a": 3}, {"a": 2}, {"a": 1}],
        )
        assert result.is_success

        # Not equal.
        result = self.json_comparator.compare_json(
            [DotWiz({"a": 1}), DotWiz({"a": 2})],
            [DotWiz({"a": 1}), DotWiz({"a": 3})],
        )
        print(result.fail_messages)
        assert not result.is_success
