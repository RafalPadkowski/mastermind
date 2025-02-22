from dataclasses import dataclass, fields
from typing import Any, Final

from .variation import Variation

LANGUAGES: Final[dict[str, str]] = {
    "en": "English",
    "pl": "Polish",
}

VARIATIONS: Final[dict[str, Variation]] = {
    "original": Variation(name="original", num_rows=10, num_pegs=4, num_colors=6),
    "mini": Variation(name="mini", num_rows=6, num_pegs=4, num_colors=6),
    "super": Variation(name="super", num_rows=12, num_pegs=5, num_colors=8),
}


@dataclass
class _Settings:
    language: str = "pl"
    variation: Variation = VARIATIONS["mini"]
    duplicate_colors: bool = False
    blank_color: bool = False

    def set(self, settings_dict: dict[str, Any]) -> None:
        for field in fields(self):
            if field.name == "variation":
                setattr(self, field.name, VARIATIONS[settings_dict[field.name]])
                continue

            setattr(self, field.name, settings_dict[field.name])


app_settings: _Settings = _Settings()
