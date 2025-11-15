from textual.widgets import Label

from .. import app_config
from ..game import Game


class Check(Label):
    def __init__(self, game: Game) -> None:
        self.game = game
        self.default_text = (
            f"{app_config.ui['check_default_text']} " * self.game.num_pegs
        )[:-1]
        self.hover_text = (
            f"{app_config.ui['check_hover_text']} " * self.game.num_pegs
        )[:-1]

        super().__init__(self.default_text, id="check", classes="check")

    def on_enter(self) -> None:
        self.update(self.hover_text)

    def on_leave(self) -> None:
        self.update(self.default_text)
