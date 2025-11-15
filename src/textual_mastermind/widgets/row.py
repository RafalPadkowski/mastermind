from textual.app import ComposeResult
from textual.containers import Horizontal
from textual.widgets import Label

from ..app_config import app_config
from .check import Check
from .code_peg import CodePeg


class Row(Horizontal):
    def __init__(self, row_number: int) -> None:
        super().__init__(classes="row")

        self.row_number = row_number

        variation = app_config.variation

        self.code_pegs: list[CodePeg] = [
            CodePeg() for _ in range(variation["num_pegs"])
        ]

        self.check: Check = Check()

    def compose(self) -> ComposeResult:
        yield Label(f"{self.row_number:02}", classes="num")
        for code_peg in self.code_pegs:
            yield code_peg
        yield self.check
