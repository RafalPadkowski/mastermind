import tomllib
from dataclasses import dataclass
from pathlib import Path

from mastermind.constants import VARIATIONS
from mastermind.variation import Variation


@dataclass
class Settings:
    language: str
    variation: Variation
    duplicate_colors: bool
    blank_color: bool


def load_settings(settings_path: Path) -> Settings:
    with settings_path.open(mode="rb") as toml_file:
        toml_data: dict = tomllib.load(toml_file)

    return Settings(
        language=toml_data["language"],
        variation=VARIATIONS[toml_data["variation"]],
        duplicate_colors=toml_data["duplicate_colors"],
        blank_color=toml_data["blank_color"],
    )
