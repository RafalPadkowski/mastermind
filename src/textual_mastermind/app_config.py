from importlib.resources import files
from typing import Any, TypedDict

import tomlkit


class Ui(TypedDict):
    main_icon: str
    new_game_icon: str
    code_blank_symbol: str
    code_symbols: list[str]
    feedback_blank_symbol: str
    feedback_symbols: list[str]


class Variation(TypedDict):
    num_rows: int
    num_pegs: int
    num_symbols: int


class Setting(TypedDict):
    default_value: Any
    current_value: Any


class VariationSetting(Setting):
    default_value: str
    current_value: str


class BlankSymbolSetting(Setting):
    default_value: bool
    current_value: bool


class DuplicateSymbolsSetting(Setting):
    default_value: bool
    current_value: bool


class AppConfig:
    def __init__(
        self, ui: Ui, variations: dict[str, Variation], settings: dict[str, Setting]
    ) -> None:
        self.ui = ui
        self.variations = variations
        self.settings = settings


with files(__package__).joinpath("config.toml").open("r", encoding="utf-8") as config:
    config_dict = tomlkit.load(config)

app_config = AppConfig(
    ui=config_dict["ui"],
    variations=config_dict["variations"],
    settings=config_dict["settings"],
)
