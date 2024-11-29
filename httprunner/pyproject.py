"""
Configurations loaded from `pyproject.toml`.

reference: _pytest/config/findpaths.py
"""

import os
import sys
from functools import cache
from pathlib import Path
from typing import Any, Callable, Union

from loguru import logger

from httprunner.builtin.dictionary import get_from_nested_dict


def get_absolute_path(path: Union[Path, str]) -> Path:
    """Convert a path to an absolute path using os.path.abspath.

    Prefer this over Path.resolve() (see #6523).
    Prefer this over Path.absolute() (not public, doesn't normalize).
    """
    return Path(os.path.abspath(str(path)))


@cache
def locate_pyproject_toml_dir() -> Path:
    """Locate project root directory by searching file `pyproject.toml` upwards from current directory."""
    current_dir = get_absolute_path(Path.cwd())
    for base in (current_dir, *current_dir.parents):
        p = base / "pyproject.toml"
        if p.is_file():
            return base

    raise FileNotFoundError(
        "file `pyproject.toml` was not found in current directory and its parents"
    )


@cache
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


def get_pyproject_toml_key_value(key: str, default: Any) -> Any:
    """Guess key value based on environment variables and `pyproject.toml`.

    :param key: Dot-separated key string.
    :param default: Default value if key was not found in `pyproject.toml`.
    """
    key_parts = key.split(".")

    try:
        config_value = get_from_nested_dict(load_pyproject_toml(), *key_parts)
    except KeyError:
        # Return value specified by `default` if key was not found in pyproject.toml.
        logger.warning(
            f"key {key} not found in pyproject.toml, the default value {repr(default)} will be used."
        )
        return default

    # Return value directly if configuration was not sourced from an environment variable.
    if not (isinstance(config_value, dict) and "env" in config_value):
        return config_value

    # Return value got from environment variable.
    if (env_var_name := config_value["env"]) in os.environ:
        return os.environ.get(env_var_name)

    # return value specified by `default`
    if "default" in config_value:
        return config_value["default"]


class PyProjectTomlKey:
    def __init__(
        self, key: str, default: Any = None, validators: list[Callable] = None
    ):
        """Initialize PyProjectTomlKey.

        :param key: Dot-separated key string.
        :param default: Default value if key was not found in `pyproject.toml`.
        :param validators: Validators to validate the value.
        """
        if validators is None:
            validators = []

        self._key = key
        self._default = default
        self._validators = validators

    def __get__(self, instance, instance_type):
        """Get value from pyproject.toml."""
        value = get_pyproject_toml_key_value(self._key, self._default)
        [validator(value) for validator in self._validators]
        return value


class PyProjectToml:
    """Project meta read from pyproject.toml."""

    http_headers: dict = PyProjectTomlKey("tool.httprunner.http-headers", {})
    request_timezones: list = PyProjectTomlKey(
        "tool.httprunner.request-timezones",
        [
            {
                "timezone": "UTC",
                "format": "%Y-%m-%d %H:%M:%S.%f %z",
            },
            {
                "timezone": "Asia/Shanghai",
                "format": "%Y-%m-%d %H:%M:%S.%f %z",
                "flag": "🇨🇳",
            },
        ],
    )
