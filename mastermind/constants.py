from pathlib import Path
from typing import Final

from textual.binding import Binding
from textual_utils import AppMetadata

from mastermind.variation import Variation

LOCALEDIR = Path(__file__).parent / "locale"

APP_METADATA = AppMetadata(
    name="Master Mind",
    version="2.0",
    codename="🔴 ⚪",
    author="Rafal Padkowski",
    email="rafaelp@poczta.onet.pl",
)

ICON: Final[str] = "❔"

SETTINGS_PATH: Final[Path] = Path(__file__).parent / "settings.toml"

LANGUAGES: Final[dict[str, str]] = {
    "en": "English",
    "pl": "Polish",
}

VARIATIONS: Final[dict[str, Variation]] = {
    "original": Variation(name="original", num_rows=10, num_pegs=4, num_colors=6),
    "mini": Variation(name="mini", num_rows=6, num_pegs=4, num_colors=6),
    "super": Variation(name="super", num_rows=12, num_pegs=5, num_colors=8),
}

BLANK_COLOR: Final[str] = "⭕"
CODE_PEG_COLORS: Final[list[str]] = ["🔴", "🟡", "🟣", "🟢", "🟤", "🔵", "⚪", "🟠"]
FEEDBACK_PEG_COLORS: Final[list[str]] = ["🔴", "⚪"]


KEY_TO_BINDING: Final[dict[str, Binding]] = {
    "ctrl+c": Binding(
        key="ctrl+c",
        action="nothing",
        description="",
    ),
    "f2": Binding(
        key="f2",
        action="new_game",
        description="New game",
        key_display="F2",
    ),
    "f3": Binding(
        key="f3",
        action="settings",
        description="Settings",
        key_display="F3",
    ),
}
