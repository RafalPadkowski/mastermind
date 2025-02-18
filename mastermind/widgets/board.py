from textual.containers import VerticalScroll

from .row import Row


class Board(VerticalScroll):
    def __init__(self) -> None:
        super().__init__(Row(row_number=1))
