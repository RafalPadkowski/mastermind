import tomllib
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import tomli_w

from mastermind.constants import VARIATIONS
from mastermind.variation import Variation


@dataclass
class Settings:
    language: str
    variation: Variation
    duplicate_colors: bool
    blank_color: bool


def load_settings(settings_path: Path) -> dict[str, Any]:
    with settings_path.open(mode="rb") as toml_file:
        toml_data: dict[str, Any] = tomllib.load(toml_file)

    return toml_data


def parse_settings(settings_dict: dict[str, Any]) -> Settings:
    variation: Variation = VARIATIONS[settings_dict.pop("variation")]

    return Settings(variation=variation, **settings_dict)


def save_settings(settings_dict: dict[str, Any], settings_path: Path) -> None:
    with settings_path.open(mode="wb") as toml_file:
        tomli_w.dump(settings_dict, toml_file)
