from httprunner.builtin.jsoncomparator.comparator import JSONComparator


class TestAllSimpleValues:
    json_comparator = JSONComparator(False)

    def test_order_different(self):
        result = self.json_comparator.compare_json([1, 2, 3], [3, 2, 1])
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

    def test_compare_true_with_1(self):
        # equal
        result = self.json_comparator.compare_json(
            {"a": [False, True]}, {"a": [True, False]}
        )
        assert result.is_success

        # equal
        result = self.json_comparator.compare_json(
            {"a": [False, True, 1, 0]}, {"a": [0, 1, True, False]}
        )
        assert result.is_success

        # not equal
        result = self.json_comparator.compare_json({"a": [False, 1]}, {"a": [0, True]})
        print(result.fail_messages)
        assert not result.is_success

    def test_simple_value_1p0_equal_1(self):
        # equal
        result = self.json_comparator.compare_json(
            {"a": [1.0, 2.0, 3.0]},
            {"a": [1, 2.0, 3]},
        )
        assert result.is_success

        # equal
        result = self.json_comparator.compare_json(
            {"a": [1.10, 2.20, 3.30]},
            {"a": [1.1, 2.2, 3.3]},
        )
        assert result.is_success

        # not equal
        result = self.json_comparator.compare_json(
            {"a": [1.1, 2.0, 3.11]},
            {"a": [1, 2.0, 3.110]},
        )
        print(result.fail_messages)
        assert not result.is_success

    def test_missing_item(self):
        # number
        result = self.json_comparator.compare_json({"a": [1, 2, 3]}, {"a": [1, 2, 2]})
        print(result.fail_messages)
        assert not result.is_success

        # bool
        result = self.json_comparator.compare_json(
            {"b": [True, False]}, {"b": [True, True]}
        )
        print(result.fail_messages)
        assert not result.is_success

    def test_unexpected_item(self):
        # number
        result = self.json_comparator.compare_json(
            {"a": [1, 2, 3, 3]}, {"a": [1, 2, 3, 4]}
        )
        print(result.fail_messages)
        assert not result.is_success

        # bool
        result = self.json_comparator.compare_json({"b": [1, 1]}, {"b": [True, False]})
        print(result.fail_messages)
        assert not result.is_success
