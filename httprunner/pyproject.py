"""
Configurations loaded from `pyproject.toml`.

reference: _pytest/config/findpaths.py
"""
import os
import sys
from pathlib import Path
from typing import Union, Any, Callable

from httprunner.builtin.dictionary import is_keys_exist, get_from_nested_dict


def get_absolute_path(path: Union[Path, str]) -> Path:
    """Convert a path to an absolute path using os.path.abspath.

    Prefer this over Path.resolve() (see #6523).
    Prefer this over Path.absolute() (not public, doesn't normalize).
    """
    return Path(os.path.abspath(str(path)))


def locate_pyproject_toml_dir() -> Path:
    """
    Locate project root directory by searching file `pyproject.toml` upwards from current directory.
    """
    current_dir = get_absolute_path(Path.cwd())
    for base in (current_dir, *current_dir.parents):
        p = base / "pyproject.toml"
        if p.is_file():
            return base

    raise FileNotFoundError(
        "file `pyproject.toml` was not found in current directory and its parents"
    )


def load_pyproject_toml() -> dict:
    """
    Load configurations from `pyproject.toml`.
    """
    # find pyproject.toml
    pyproject_toml_file = locate_pyproject_toml_dir() / "pyproject.toml"

    if sys.version_info >= (3, 11):
        import tomllib  # noqa
    else:
        import tomli as tomllib  # noqa

    # load pyproject.toml
    toml_text = pyproject_toml_file.read_text(encoding="utf-8")
    return tomllib.loads(toml_text)


def is_key_exists(pyproject_toml_: dict, toml_key: str) -> bool:
    """
    Check if specific key of `pyproject.toml` exists.

    :param pyproject_toml_: data loaded from `pyproject.toml`
    :param toml_key: key in toml, e.g. `tool.httprunner.foo`
    """
    return is_keys_exist(pyproject_toml_, *toml_key.split("."))


def get_pyproject_toml_key_value(
    pyproject_toml_data_: dict, key: str, is_key_required: bool = True
) -> Any:
    """Guess key value based on environment variables and `pyproject.toml`."""
    # make sure nested keys exist
    if is_key_required and not is_key_exists(pyproject_toml_data_, key):
        raise KeyError(f"key `{key}` does not exist in pyproject.toml")

    key_parts = key.split(".")
    config_value = get_from_nested_dict(pyproject_toml_data_, *key_parts)

    # return value directly if configuration was not sourced from an environment variable
    if not (isinstance(config_value, dict) and "env" in config_value):
        return config_value

    # return value got from environment variable
    env_var_name = config_value["env"]
    if env_var_name in os.environ:
        return os.environ.get(env_var_name)

    # return value specified by `default`
    if "default" in config_value:
        return config_value["default"]

    raise KeyError(
        f"environment variable `{env_var_name}` was not set.\n"
        f"Hint: set environment variable `{env_var_name}` or add key `default` to specify configuration"
    )


class PyProjectTomlKey:
    def __init__(
        self,
        pyproject_toml_data_: dict,
        key: str,
        is_required: bool,
        *validators: Callable,
    ):
        self._pyproject_toml_data = pyproject_toml_data_
        self._key = key
        self._is_required = is_required
        self._validators = validators

    def __get__(self, instance, instance_type):
        """
        Get value from pyproject.toml.
        """
        value = get_pyproject_toml_key_value(
            self._pyproject_toml_data, self._key, self._is_required
        )
        [validator(value) for validator in self._validators]
        return value


pyproject_toml_data = load_pyproject_toml()


class HttpRunnerProjectMeta:
    """
    Project meta read from pyproject.toml.
    """

    http_headers: PyProjectTomlKey = PyProjectTomlKey(
        pyproject_toml_data, "tool.httprunner.http-headers", False
    )


httprunner_project_meta = HttpRunnerProjectMeta()
