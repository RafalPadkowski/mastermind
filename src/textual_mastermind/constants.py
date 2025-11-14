from pathlib import Path
from typing import Final

from textual.binding import Binding

LOCALE_DIR: Final[Path] = Path(__file__).parent / "locale"

CONFIG_FILE: Final[Path] = Path(__file__).parent / "config.toml"

KEY_TO_BINDING: Final[dict[str, Binding]] = {
    "ctrl+q": Binding(
        key="ctrl+q",
        action="quit",
        description="Quit",
        key_display="Ctrl+Q",
        show=True,
    ),
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
