import dataclasses

from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Vertical
from textual.widgets import Select
from textual.widgets._select import SelectOverlay

from ..app_config import app_config


class ColorSelect(Select[int]):
    def __init__(self) -> None:
        variation = app_config.variation

        super().__init__(
            options=zip(
                app_config.ui["code_peg_colors"], range(1, variation["num_colors"] + 1)
            ),
            prompt=app_config.ui["blank_color"],
        )

    def on_mount(self) -> None:
        select_overlay = self.query_one(SelectOverlay)

        esc_binding: Binding = select_overlay._bindings.key_to_bindings["escape"][0]
        select_overlay._bindings.key_to_bindings["escape"] = [
            dataclasses.replace(esc_binding, show=False)
        ]


class Panel(Vertical):
    def compose(self) -> ComposeResult:
        yield ColorSelect()
