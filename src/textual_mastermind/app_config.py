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
    feedback_blank_letters: str
    feedback_letters: list[str]
    feedback_colors: list[str]


class Variation(TypedDict):
    num_rows: int
    num_pegs: int
    num_colors: int


class Setting(TypedDict):
    default_value: Any
    current_value: Any


class AppConfig:
    def __init__(
        self, ui: Ui, variations: dict[str, Variation], settings: dict[str, Setting]
    ) -> None:
        self.ui = ui
        self.variations = variations
        self.settings = settings

    @property
    def current_variation(self) -> Variation:
        return self.variations[self.settings["variation"]["current_value"]]

    @property
    def blank_color(self) -> bool:
        return self.settings["blank_color"]["current_value"]

    @property
    def duplicate_colors(self) -> bool:
        return self.settings["duplicate_colors"]["current_value"]


with files(__package__).joinpath("config.toml").open("r", encoding="utf-8") as config:
    config_dict = tomlkit.load(config)

app_config = AppConfig(
    ui=config_dict["ui"],
    variations=config_dict["variations"],
    settings=config_dict["settings"],
)
