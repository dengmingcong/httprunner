import json
from typing import List, Union

from deepdiff import DeepDiff
from deepdiff.model import DiffLevel


def convert_path_to_jmespath(path: list, data: Union[list, dict]) -> str:
    """
    Convert deepdiff path to jmes path.

    >>> convert_path_to_jmespath([1, 'a'], [{"a": 1}, {"a": 1, "b": 2}])
    '[1].a'
    """
    jmespath = ""
    for index, item in enumerate(path):
        if isinstance(data, list):
            jmespath += f"[{item}]"
            data = data[item]
        elif isinstance(data, dict):
            jmespath += f".{item}"
            data = data[item]

        if not isinstance(data, (list, dict)) and index != len(path) - 1:
            raise ValueError(
                f"path have not been iterated over, but non-compound value {data} got, "
                f"current jmespath: {jmespath}"
            )
    return jmespath.lstrip(".")


class DeepDiffFormatter(object):
    """
    Formatter for JSONassert.

    Note: all format methods treat 't1' as value expected, 't2' as value got.
    """

    def __init__(self, strict: bool, ddiff: DeepDiff):
        """
        Init formatter.
        :param strict: bool
        :param ddiff: view MUST be 'tree', the first item to be compared MUST be the expected value,
        """
        self.strict = strict
        self.ddiff = ddiff
        self.fail_match_iterable_paths: List[str] = []
        self.formatted_string = ""
        assert ddiff.view == "tree", "The DeepDiff View MUST be set to 'tree'."

    def format_type_changes(self):
        """Format 'type_changes'."""
        if "type_changes" in self.ddiff:
            self.formatted_string += "\n** Type Changes **"

            type_changes_list = list(self.ddiff["type_changes"])
            for type_changes in type_changes_list:
                path = convert_path_to_jmespath(
                    type_changes.path(output_format="list"), self.ddiff.t1
                )
                t1 = type_changes.t1
                t1_type = type(t1).__name__
                t2 = type_changes.t2
                t2_type = type(t2).__name__

                self.formatted_string += f"\n  - jmespath: {path}\n"
                self.formatted_string += f"    expected: {t1_type:10} {t1}\n"
                self.formatted_string += f"         got: {t2_type:10} {t2}"

            self.formatted_string += "\n"

    def format_values_changed(self):
        """Format 'values_changed'."""
        if "values_changed" in self.ddiff:
            self.formatted_string += "\n** Value Changes **"

            values_changed_list = list(self.ddiff["values_changed"])
            for value_changed in values_changed_list:
                path = convert_path_to_jmespath(
                    value_changed.path(output_format="list"), self.ddiff.t1
                )
                t1 = value_changed.t1
                t2 = value_changed.t2

                self.formatted_string += f"\n  - jmespath: {path}\n"
                self.formatted_string += f"    expected: {t1}\n"
                self.formatted_string += f"         got: {t2}"

            self.formatted_string += "\n"

    def format_dictionary_item_added(self):
        """Format dictionary_item_added."""
        if "dictionary_item_added" in self.ddiff:
            self.formatted_string += "\nThese dictionary items are not expected:"

            added_dict_items = list(self.ddiff["dictionary_item_added"])
            for added_item in added_dict_items:
                path = convert_path_to_jmespath(
                    added_item.path(output_format="list"), self.ddiff.t2
                )
                t2 = added_item.t2
                self.formatted_string += f"\n    jmespath: {path}, value: {t2}"

            self.formatted_string += "\n"

    def format_dictionary_item_removed(self):
        """Format dictionary_item_removed."""
        if "dictionary_item_removed" in self.ddiff:
            self.formatted_string += "\nThese dictionary items are missing:"

            removed_dict_items = list(self.ddiff["dictionary_item_removed"])
            for removed_item in removed_dict_items:
                path = convert_path_to_jmespath(
                    removed_item.path(output_format="list"), self.ddiff.t1
                )
                t1 = removed_item.t1
                t1_type = type(t1).__name__
                self.formatted_string += f"\n    jmespath: {path}, type expected: {t1_type}, value expected: {t1}"

            self.formatted_string += "\n"

    def format_iterable_parent(self, child: DiffLevel):
        """Print the parent element of iterable to simplify output."""
        parent = child.up
        parent_path = convert_path_to_jmespath(
            parent.path(output_format="list"), self.ddiff.t1
        )
        omit_length = 500

        if parent_path not in self.fail_match_iterable_paths:
            self.fail_match_iterable_paths.append(parent_path)
            if len(parent.t1) != len(parent.t2):
                self.formatted_string += (
                    f"\n  - jmespath: {parent_path}, expected {len(parent.t1)} "
                    f"but got {len(parent.t2)}"
                )
            if len((t1 := json.dumps(parent.t1, ensure_ascii=False))) > omit_length:
                t1 = t1[:omit_length] + "..."
            if len((t2 := json.dumps(parent.t2, ensure_ascii=False))) > omit_length:
                t2 = t2[:omit_length] + "..."
            self.formatted_string += f"\n    list expected: {t1}"
            self.formatted_string += f"\n    list got: {t2}"
        else:
            return

    def format_iterable(self):
        """Format iterable_item_added, iterable_item_removed and repetition_change."""
        if (
            "iterable_item_added" in self.ddiff
            or "iterable_item_removed" in self.ddiff
            or "repetition_change" in self.ddiff
        ):
            self.formatted_string += "\nThese lists are not expected:"

            if "iterable_item_added" in self.ddiff:
                added_iterable_items = list(self.ddiff["iterable_item_added"])
                for added_item in added_iterable_items:
                    self.format_iterable_parent(added_item)

            if "iterable_item_removed" in self.ddiff:
                removed_iterable_items = list(self.ddiff["iterable_item_removed"])
                for removed_item in removed_iterable_items:
                    self.format_iterable_parent(removed_item)

            if "repetition_change" in self.ddiff:
                repetition_items = list(self.ddiff["repetition_change"])
                for repetition_item in repetition_items:
                    self.format_iterable_parent(repetition_item)

    def format(self):
        """Format for all changes."""
        postfix = "STRICT mode" if self.strict else "NON-STRICT mode"

        self.formatted_string += f"compare result in {postfix}:\n"
        self.format_type_changes()
        self.format_values_changed()

        if self.strict:
            self.format_dictionary_item_added()

        self.format_dictionary_item_removed()
        self.format_iterable()
