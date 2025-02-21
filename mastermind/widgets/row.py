from textual.containers import Horizontal
from textual.widgets import Button, Label

from mastermind.settings import app_settings
from mastermind.widgets.code_peg import CodePeg


class Row(Horizontal):
    def __init__(self, row_number: int) -> None:
        num_pegs: int = app_settings.variation.num_pegs
        self.code_pegs: list[CodePeg] = [CodePeg() for _ in range(num_pegs)]

        self.check_button: Button = Button("❔", classes="check", id="check")

        super().__init__(
            Label(f"{row_number:02}", classes="num"),
            *self.code_pegs,
            self.check_button,
            classes="row",
        )
