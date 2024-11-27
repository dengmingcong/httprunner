from httprunner.builtin.jsoncomparator.comparator import JSONComparator


class TestJsonComparatorLenientMode:
    json_comparator = JSONComparator(False)

    def test_invalid_json_data_type(self):
        result = self.json_comparator.compare_json((1, 2), [1, 2])
        print(result.fail_messages)
        assert not result.is_success

        result = self.json_comparator.compare_json([1, 2], (1, 2))
        print(result.fail_messages)
        assert not result.is_success

    def test_1_equal_1p0(self):
        result = self.json_comparator.compare_json(1.0, 1)
        assert result.is_success

    def test_compare_true_with_1(self):
        result = self.json_comparator.compare_json(1, True)
        print(result.fail_messages)
        assert not result.is_success

        result = self.json_comparator.compare_json(0, False)
        print(result.fail_messages)
        assert not result.is_success

    def test_compare_simple_value_int(self):
        # equal
        result = self.json_comparator.compare_json(1, 1)
        assert result.is_success

        # not equal
        result = self.json_comparator.compare_json(1, 2)
        print(result.fail_messages)
        assert not result.is_success

    def test_compare_simple_value_float(self):
        # equal
        result = self.json_comparator.compare_json(1.25, 1.25)
        assert result.is_success

        # not equal
        result = self.json_comparator.compare_json(1.25, 1.26)
        print(result.fail_messages)
        assert not result.is_success

    def test_compare_simple_value_str(self):
        # equal
        result = self.json_comparator.compare_json("abc", "abc")
        assert result.is_success

        # not equal
        result = self.json_comparator.compare_json("abc", "def")
        print(result.fail_messages)
        assert not result.is_success

    def test_compare_simple_value_bool(self):
        # equal
        result = self.json_comparator.compare_json(True, True)
        assert result.is_success

        # not equal
        result = self.json_comparator.compare_json(True, False)
        print(result.fail_messages)
        assert not result.is_success

    def test_compare_simple_value_null(self):
        # equal
        result = self.json_comparator.compare_json(None, None)
        assert result.is_success

        # not equal
        result = self.json_comparator.compare_json(None, "null")
        print(result.fail_messages)
        assert not result.is_success

    def test_compare_json_objects_equal(self):
        result = self.json_comparator.compare_json({"a": 1, "b": 2}, {"a": 1, "b": 2})
        assert result.is_success

    def test_compare_json_objects_missing_key(self):
        result = self.json_comparator.compare_json({"a": 1, "b": 2}, {"a": 1})
        print(result.fail_messages)
        assert not result.is_success

    def test_compare_json_objects_not_equal(self):
        result = self.json_comparator.compare_json({"a": 1, "b": 2}, {"a": 1, "b": 3})
        print(result.fail_messages)
        assert not result.is_success

    def test_compare_json_objects_nested_not_equal(self):
        result = self.json_comparator.compare_json(
            {"a": 1, "b": {"c": 2, "d": 3}}, {"a": 1, "b": {"c": 2, "d": 4}}
        )
        print(result.fail_messages)
        assert not result.is_success

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
