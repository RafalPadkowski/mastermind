from pathlib import Path
from typing import Final

from textual.binding import Binding

from mastermind.variation import Variation

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
    "ctrl+q": Binding(
        key="ctrl+q",
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
    "f12": Binding(
        key="f12",
        action="quit",
        description="Quit",
        key_display="F12",
    ),
}
