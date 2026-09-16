from importlib.resources import files
from typing import Any, TypedDict

import tomlkit


class Ui(TypedDict):
    main_icon: str
    new_game_icon: str
    code_blank_letter: str
    code_letters: list[str]
    code_colors: list[str]
    code_style: str
    feedback_blank_letter: str
    feedback_letters: list[str]
    feedback_colors: list[str]
    feedback_style: str


class Variation(TypedDict):
    num_rows: int
    num_pegs: int
    num_colors: int


class Setting(TypedDict):
    default_value: Any
    current_value: Any


class Settings(TypedDict):
    variation: Setting
    allow_blank_color: Setting
    allow_duplicate_colors: Setting


class AppConfig:
    def __init__(
        self, ui: Ui, variations: dict[str, Variation], settings: Settings
    ) -> None:
        self.ui = ui
        self.variations = variations
        self.settings = settings

    @property
    def variation(self) -> Variation:
        return self.variations[self.settings["variation"]["current_value"]]

    @property
    def allow_blank_color(self) -> bool:
        return self.settings["allow_blank_color"]["current_value"]

    @property
    def allow_duplicate_colors(self) -> bool:
        return self.settings["allow_duplicate_colors"]["current_value"]


with files(__package__).joinpath("config.toml").open("r", encoding="utf-8") as config:
    config_dict = tomlkit.load(config)

app_config = AppConfig(
    ui=config_dict["ui"],
    variations=config_dict["variations"],
    settings=config_dict["settings"],
)
