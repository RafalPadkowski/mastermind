import tomllib
from dataclasses import dataclass
from pathlib import Path

from mastermind.config import Variation, app_config


@dataclass
class Settings:
    variation: Variation
    blank_color: bool
    duplicate_colors: bool


settings_filename = app_config.general.settings_filename
settings_path = Path(__file__).parent / settings_filename
with settings_path.open(mode="rb") as toml_file:
    toml_data: dict = tomllib.load(toml_file)

app_settings = Settings(
    variation=app_config.variations[toml_data["variation"]],
    blank_color=toml_data["blank_color"],
    duplicate_colors=toml_data["duplicate_colors"],
)
