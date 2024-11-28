from httprunner.builtin.jsoncomparator.comparator import JSONComparator


class TestAllJSONObjects:
    json_comparator = JSONComparator(False)

    def test_unique_key_usable_and_equal(self):
        result = self.json_comparator.compare_json(
            [{"a": 1}, {"a": 2}, {"a": 3}], [{"a": 3}, {"a": 2}, {"a": 1}]
        )
        assert result.is_success
