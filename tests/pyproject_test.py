from typing import Any

import pytest

from httprunner.pyproject import PyProjectTomlKey, load_pyproject_toml


class TestPyProjectToml:
    def test_additional_validator(self):
        def name_must_be_str(v: Any):
            if not isinstance(v, str):
                raise TypeError

        # expect to fail
        def name_must_be_int(v: Any):
            if not isinstance(v, int):
                raise TypeError

        class CorrectProjectMeta:
            name = PyProjectTomlKey(
                load_pyproject_toml(), "tool.poetry.name", name_must_be_str
            )

        class IncorrectProjectMeta:
            name = PyProjectTomlKey(
                load_pyproject_toml(),
                "tool.poetry.name",
                name_must_be_str,
                name_must_be_int,
            )

        assert CorrectProjectMeta().name == "httprunner"
        with pytest.raises(TypeError):
            assert IncorrectProjectMeta().name == "httprunner"
