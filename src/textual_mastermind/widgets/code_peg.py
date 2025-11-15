import dataclasses

from textual.binding import Binding
from textual.widgets import Select
from textual.widgets._select import SelectOverlay

from .. import app_config
from ..game import Game


class CodePeg(Select[int]):
    def __init__(self, game: Game) -> None:
        self.game = game

        super().__init__(
            options=zip(
                app_config.ui["code_peg_colors"], range(1, self.game.num_colors + 1)
            ),
            prompt=app_config.ui["blank_color"],
            classes="code_peg",
        )

    def on_mount(self) -> None:
        option_list = self.query_one(SelectOverlay)

        esc_binding: Binding = option_list._bindings.key_to_bindings["escape"][0]
        option_list._bindings.key_to_bindings["escape"] = [
            dataclasses.replace(esc_binding, show=False)
        ]
