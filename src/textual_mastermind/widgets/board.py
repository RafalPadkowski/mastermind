from textual.app import ComposeResult
from textual.containers import Horizontal, VerticalScroll
from textual.widgets import Button, Label

from ..app_config import app_config


class Row(Horizontal):
    def __init__(self, row_number: int) -> None:
        super().__init__(classes="row")

        self.row_number = row_number

        self.code_pegs: list[Button] = [
            Button(
                flat=True, label=app_config.ui["code_blank_letter"], classes="code_peg"
            )
            for _ in range(app_config.current_variation["num_pegs"])
        ]

        self.check: Button = Button(flat=True, label="?", classes="check")

    def compose(self) -> ComposeResult:
        yield Label(f"{self.row_number:02}", classes="num")
        yield from self.code_pegs
        yield self.check


class Board(VerticalScroll):
    def __init__(self) -> None:
        super().__init__()

        self.current_row_number = 1
        self.current_row = Row(row_number=self.current_row_number)

    def compose(self) -> ComposeResult:
        yield self.current_row

    def add_row(self):
        self.current_row_number += 1
        self.current_row = Row(row_number=self.current_row_number)
        self.mount(self.current_row)
        self.scroll_end()
