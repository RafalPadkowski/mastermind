import tomllib
from dataclasses import dataclass
from pathlib import Path


@dataclass
class Settings:
    language: str
    variation: str
    blank_color: bool
    duplicate_colors: bool


def load_settings(settings_path: Path) -> Settings:
    with settings_path.open(mode="rb") as toml_file:
        toml_data: dict = tomllib.load(toml_file)

    return Settings(**toml_data)
