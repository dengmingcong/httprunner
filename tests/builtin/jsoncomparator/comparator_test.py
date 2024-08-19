from httprunner.builtin.jsoncomparator.comparator import JSONComparator


class TestJsonComparatorLenientMode:
    json_comparator = JSONComparator(False)

    def test_invalid_json_data_type(self):
        result = self.json_comparator.compare_json((1, 2), [1, 2])
        print(result.fail_messages)
        assert not result.is_success

    def test_two_numbers(self):
        result = self.json_comparator.compare_json(1.0, 1)
        print(result.fail_messages)
        assert result.is_success

    def test_compare_true_with_1(self):
        result = self.json_comparator.compare_json(True, 1)
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
