import tomllib
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import tomli_w

from mastermind.constants import VARIATIONS
from mastermind.variation import Variation


@dataclass
class Settings:
    language: str = "en"
    variation: Variation = VARIATIONS["mini"]
    duplicate_colors: bool = False
    blank_color: bool = False


_app_settings: Settings


def load_settings(settings_path: Path) -> dict[str, Any]:
    with settings_path.open(mode="rb") as toml_file:
        settings_dict: dict[str, Any] = tomllib.load(toml_file)

    return settings_dict


def set_settings(settings_dict: dict[str, Any]) -> None:
    global _app_settings

    _app_settings = Settings(
        variation=VARIATIONS[settings_dict["variation"]],
        **{key: value for key, value in settings_dict.items() if key != "variation"},
    )


def get_settings() -> Settings:
    global _app_settings

    return _app_settings


def save_settings(settings_dict: dict[str, Any], settings_path: Path) -> None:
    with settings_path.open(mode="wb") as toml_file:
        tomli_w.dump(settings_dict, toml_file)
