from dataclasses import dataclass, fields
from typing import Any

from mastermind.constants import VARIATIONS
from mastermind.variation import Variation


@dataclass
class _Settings:
    language: str = "pl"
    variation: Variation = VARIATIONS["mini"]
    duplicate_colors: bool = False
    blank_color: bool = False


app_settings: _Settings = _Settings()


def set_settings(settings_dict: dict[str, Any]) -> None:
    for field in fields(app_settings):
        if field.name == "variation":
            setattr(app_settings, field.name, VARIATIONS[settings_dict[field.name]])
            continue

        setattr(app_settings, field.name, settings_dict[field.name])
