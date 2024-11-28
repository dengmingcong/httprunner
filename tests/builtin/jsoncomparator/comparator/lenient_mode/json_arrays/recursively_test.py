from httprunner.builtin.jsoncomparator.comparator import JSONComparator


class TestRecursively:
    json_comparator = JSONComparator(False)

    def test_all_kinds_data_and_equal(self):
        result = self.json_comparator.compare_json(
            [1, 2.2, "abc", True, False, {"a": 1}, [1, 2, 3], None],
            [None, [1, 2, 3], {"a": 1}, False, True, "abc", 2.2, 1],
        )
        assert result.is_success

    def test_item_is_invalid_json_data_type(self):
        # Expected item.
        result = self.json_comparator.compare_json([(1, 2), 3], [3, (1, 2)])
        print(result.fail_messages)
        assert not result.is_success

        # Actual item.
        result = self.json_comparator.compare_json([1, 2], [(1, 2), 3])
        print(result.fail_messages)
        assert not result.is_success

    def test_1p0_equals_1(self):
        result = self.json_comparator.compare_json(
            [1.0, {}, []],
            [{}, [], 1],
        )
        assert result.is_success

    def test_true_not_equal_1(self):
        result = self.json_comparator.compare_json([True, {}], [{}, 1])
        print(result.fail_messages)
        assert not result.is_success

        result = self.json_comparator.compare_json([{}, 1], [True, {}])
        print(result.fail_messages)
        assert not result.is_success

    def test_print_string_not_found(self):
        result = self.json_comparator.compare_json(["foo", {}], [{}, "bar"])
        print(result.fail_messages)
        assert not result.is_success

    def test_array_of_arrays(self):
        expected = {"id": 1, "stuff": [[4, 3], [3, 2], [], [1, 2]]}
        actual = {"id": 1, "stuff": [[1, 2], [2, 3], [], [3, 4]]}
        result = self.json_comparator.compare_json(expected, actual)
        assert result.is_success
