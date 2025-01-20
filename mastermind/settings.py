import tomllib
from dataclasses import dataclass
from pathlib import Path

from mastermind.constants import VARIATIONS
from mastermind.variation import Variation


@dataclass
class Settings:
    variation: Variation
    blank_color: bool
    duplicate_colors: bool


def load_settings(settings_path: Path) -> Settings:
    with settings_path.open(mode="rb") as toml_file:
        toml_data: dict = tomllib.load(toml_file)

    return Settings(
        variation=VARIATIONS[toml_data["variation"]],
        blank_color=toml_data["blank_color"],
        duplicate_colors=toml_data["duplicate_colors"],
    )
