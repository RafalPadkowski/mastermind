from dataclasses import dataclass

from config.settings import SettingBoolean, SettingOptions


@dataclass
class Ui:
    icon: str
    blank_color: str
    code_peg_colors: list[str]
    feedback_peg_colors: list[str]
    check_default_text: str
    check_hover_text: str


@dataclass
class Settings:
    language: SettingOptions
    variation: SettingOptions
    duplicate_colors: SettingBoolean
    blank_color: SettingBoolean


@dataclass
class Variation:
    num_rows: int
    num_pegs: int
    num_colors: int
