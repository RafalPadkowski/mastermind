from textual.containers import Horizontal
from textual.widgets import Button, Label

from .code_peg import CodePeg


class Row(Horizontal):
    def __init__(self, row_number: int) -> None:
        # num_pegs: int = current_app.settings.variation.num_pegs
        num_pegs = 4

        code_pegs = [CodePeg() for _ in range(num_pegs)]

        super().__init__(
            Label(f"{row_number:02}", classes="num"),
            *code_pegs,
            Button("❔", classes="check"),
            classes="row",
        )
