from typing import Final

from textual.binding import Binding

GlOBAL_BINDINGS: Final[dict[str, Binding]] = {
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
