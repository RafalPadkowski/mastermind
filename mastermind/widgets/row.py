from textual.containers import Horizontal
from textual.widgets import Button, Label

from mastermind.settings import Settings, get_settings

from .code_peg import CodePeg


class Row(Horizontal):
    def __init__(self, row_number: int) -> None:
        app_settings: Settings = get_settings()
        num_pegs: int = app_settings.variation.num_pegs

        code_pegs = [CodePeg() for _ in range(num_pegs)]

        super().__init__(
            Label(f"{row_number:02}", classes="num"),
            *code_pegs,
            Button("❔", classes="check"),
            classes="row",
        )
