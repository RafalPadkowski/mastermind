from textual.app import ComposeResult
from textual.containers import Horizontal
from textual.widgets import Label

from ..game import Game
from .check import Check
from .code_peg import CodePeg


class Row(Horizontal):
    def __init__(self, game: Game, row_number: int) -> None:
        super().__init__(classes="row")

        self.game = game

        self.row_number = row_number

        self.code_pegs: list[CodePeg] = [
            CodePeg(self.game) for _ in range(self.game.num_pegs)
        ]

        self.check: Check = Check(self.game)

    def compose(self) -> ComposeResult:
        yield Label(f"{self.row_number:02}", classes="num")
        for code_peg in self.code_pegs:
            yield code_peg
        yield self.check
