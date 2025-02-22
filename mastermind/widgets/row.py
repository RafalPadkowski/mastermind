from textual.app import ComposeResult
from textual.containers import Horizontal
from textual.widgets import Button, Label

from mastermind.settings import app_settings
from mastermind.widgets.code_peg import CodePeg


class Row(Horizontal):
    def __init__(self, row_number: int) -> None:
        super().__init__(classes="row")

        self.row_number = row_number

        num_pegs: int = app_settings.variation.num_pegs
        self.code_pegs: list[CodePeg] = [CodePeg() for _ in range(num_pegs)]

        self.check_button: Button = Button("❔", classes="check", id="check")

    def compose(self) -> ComposeResult:
        yield Label(f"{self.row_number:02}", classes="num")
        for code_peg in self.code_pegs:
            yield code_peg
        yield self.check_button
