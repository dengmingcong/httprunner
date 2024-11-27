from httprunner.builtin.jsoncomparator.comparator import JSONComparator

json_comparator = JSONComparator(False)


def test_invalid_json_data_type():
    result = json_comparator.compare_json((1, 2), [1, 2])
    print(result.fail_messages)
    assert not result.is_success

    result = json_comparator.compare_json([1, 2], (1, 2))
    print(result.fail_messages)
    assert not result.is_success


def test_1_equal_1p0():
    result = json_comparator.compare_json(1.0, 1)
    assert result.is_success


def test_compare_true_with_1():
    result = json_comparator.compare_json(1, True)
    print(result.fail_messages)
    assert not result.is_success

    result = json_comparator.compare_json(0, False)
    print(result.fail_messages)
    assert not result.is_success


class TestCompareSimpleValue:
    json_comparator = JSONComparator(False)

    def test_int(self):
        # equal
        result = self.json_comparator.compare_json(1, 1)
        assert result.is_success

        # not equal
        result = self.json_comparator.compare_json(1, 2)
        print(result.fail_messages)
        assert not result.is_success

    def test_float(self):
        # equal
        result = self.json_comparator.compare_json(1.25, 1.25)
        assert result.is_success

        # not equal
        result = self.json_comparator.compare_json(1.25, 1.26)
        print(result.fail_messages)
        assert not result.is_success

    def test_str(self):
        # equal
        result = self.json_comparator.compare_json("abc", "abc")
        assert result.is_success

        # not equal
        result = self.json_comparator.compare_json("abc", "def")
        print(result.fail_messages)
        assert not result.is_success

    def test_bool(self):
        # equal
        result = self.json_comparator.compare_json(True, True)
        assert result.is_success

        # not equal
        result = self.json_comparator.compare_json(True, False)
        print(result.fail_messages)
        assert not result.is_success

    def test_null(self):
        # equal
        result = self.json_comparator.compare_json(None, None)
        assert result.is_success

        # not equal
        result = self.json_comparator.compare_json(None, "null")
        print(result.fail_messages)
        assert not result.is_success
