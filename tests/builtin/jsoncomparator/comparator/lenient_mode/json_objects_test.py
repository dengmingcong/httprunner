from httprunner.builtin.jsoncomparator.comparator import JSONComparator

json_comparator = JSONComparator(False)


class TestCompareJSONObjects:
    json_comparator = JSONComparator(False)

    def test_equal(self):
        result = self.json_comparator.compare_json({"a": 1, "b": 2}, {"a": 1, "b": 2})
        assert result.is_success

    def test_field_is_invalid_json_data_type(self):
        result = json_comparator.compare_json(
            {"a": (1, 2), "b": 2}, {"a": [1, 2], "b": 2}
        )
        print(result.fail_messages)
        assert not result.is_success

        result = json_comparator.compare_json(
            {"a": [1, 2], "b": 2}, {"a": (1, 2), "b": 2}
        )
        print(result.fail_messages)
        assert not result.is_success

    def test_1_equal_1p0(self):
        result = json_comparator.compare_json({"a": 1.0, "b": 2}, {"a": 1, "b": 2})
        assert result.is_success

    def test_compare_true_with_1(self):
        result = json_comparator.compare_json({"a": 1, "b": True}, {"a": 1, "b": 1})
        print(result.fail_messages)
        assert not result.is_success

        result = json_comparator.compare_json({"a": 1, "b": False}, {"a": 1, "b": 0})
        print(result.fail_messages)
        assert not result.is_success

    def test_compare_simple_values_int(self):
        # equal
        result = json_comparator.compare_json({"a": 1, "b": 2}, {"a": 1, "b": 2})
        assert result.is_success

        # not equal
        result = json_comparator.compare_json({"a": 1, "b": 2}, {"a": 1, "b": 3})
        print(result.fail_messages)
        assert not result.is_success

    def test_compare_simple_values_float(self):
        # equal
        result = json_comparator.compare_json(
            {"a": 1.25, "b": 2.5}, {"a": 1.25, "b": 2.5}
        )
        assert result.is_success

        # not equal
        result = json_comparator.compare_json(
            {"a": 1.25, "b": 2.5}, {"a": 1.251, "b": 2.6}
        )
        print(result.fail_messages)
        assert not result.is_success

    def test_compare_simple_values_str(self):
        # equal
        result = json_comparator.compare_json(
            {"a": "abc", "b": "def"}, {"a": "abc", "b": "def"}
        )
        assert result.is_success

        # not equal
        result = json_comparator.compare_json(
            {"a": "abc", "b": "def"}, {"a": "abc", "b": "xyz"}
        )
        print(result.fail_messages)
        assert not result.is_success

    def test_compare_simple_values_bool(self):
        # equal
        result = json_comparator.compare_json(
            {"a": True, "b": False}, {"a": True, "b": False}
        )
        assert result.is_success

        # not equal
        result = json_comparator.compare_json(
            {"a": True, "b": False}, {"a": True, "b": True}
        )
        print(result.fail_messages)
        assert not result.is_success

    def test_compare_simple_values_null(self):
        # equal
        result = json_comparator.compare_json(
            {"a": None, "b": None}, {"a": None, "b": None}
        )
        assert result.is_success

        # not equal
        result = json_comparator.compare_json(
            {"a": None, "b": None}, {"a": None, "b": "null"}
        )
        print(result.fail_messages)
        assert not result.is_success

    def test_compare_json_objects(self):
        # equal
        result = json_comparator.compare_json(
            {"a": {"b": 1, "c": 2}, "d": 3}, {"a": {"b": 1, "c": 2}, "d": 3}
        )
        assert result.is_success

        # not equal
        result = json_comparator.compare_json(
            {"a": {"b": 1, "c": 2}, "d": 3}, {"a": {"b": 2, "c": 3}, "d": 4}
        )
        print(result.fail_messages)
        assert not result.is_success

    def test_missing_key(self):
        result = self.json_comparator.compare_json({"a": 1, "b": 2}, {"a": 1})
        print(result.fail_messages)
        assert not result.is_success

    def test_nested_not_equal(self):
        result = self.json_comparator.compare_json(
            {"a": 1, "b": {"c": 2, "d": 3}}, {"a": 1, "b": {"c": 2, "d": 4}}
        )
        print(result.fail_messages)
        assert not result.is_success
