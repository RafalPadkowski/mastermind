from pathlib import Path
from typing import Any, TypedDict

import tomlkit
from tomlkit.toml_document import TOMLDocument


class Ui(TypedDict):
    main_icon: str
    title: str
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


class Variations(TypedDict):
    original: Variation
    mini: Variation
    super: Variation


class Setting(TypedDict):
    default_value: Any
    current_value: Any


class Settings(TypedDict):
    variation_name: Setting
    allow_blank_color: Setting
    allow_duplicate_colors: Setting


class AppConfig:
    def __init__(self, config_path: Path) -> None:
        self.config_path = config_path

        config_dict = self.load_config(self.config_path)

        self.ui: Ui = config_dict["ui"]
        self.variations: Variations = config_dict["variations"]
        self.settings: Settings = config_dict["settings"]

    def load_config(self, config_path: Path) -> TOMLDocument:
        with config_path.open("r", encoding="utf-8") as config_content:
            config_dict = tomlkit.load(config_content)

        return config_dict

    @property
    def variation_name(self) -> str:
        return self.settings["variation_name"]["current_value"]

    @variation_name.setter
    def variation_name(self, value: str) -> None:
        self.settings["variation_name"]["current_value"] = value

    @property
    def variation(self) -> Variation:
        return self.variations[self.settings["variation_name"]["current_value"]]

    @property
    def allow_blank_color(self) -> bool:
        return self.settings["allow_blank_color"]["current_value"]

    @allow_blank_color.setter
    def allow_blank_color(self, value: bool) -> None:
        self.settings["allow_blank_color"]["current_value"] = value

    @property
    def allow_duplicate_colors(self) -> bool:
        return self.settings["allow_duplicate_colors"]["current_value"]

    @allow_duplicate_colors.setter
    def allow_duplicate_colors(self, value: bool) -> None:
        self.settings["allow_duplicate_colors"]["current_value"] = value

    def save_settings(self, *settings: str) -> None:
        if not settings:
            return

        with self.config_path.open("r", encoding="utf-8") as config_content:
            config_dict = tomlkit.load(config_content)

        for setting in settings:
            config_dict["settings"][setting]["current_value"] = self.settings[setting][
                "current_value"
            ]

        with self.config_path.open("w", encoding="utf-8") as config_content:
            tomlkit.dump(config_dict, config_content)


app_config = AppConfig(config_path=Path(__file__).parent / "config.toml")
