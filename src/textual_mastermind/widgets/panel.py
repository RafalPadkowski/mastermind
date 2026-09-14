from rich.text import Text
from textual.app import ComposeResult
from textual.containers import Horizontal, VerticalScroll
from textual.widgets import Button, Select

from ..app_config import app_config


class Panel(VerticalScroll):
    def __init__(self) -> None:
        super().__init__()

    def compose(self) -> ComposeResult:
        code_symbols = app_config.ui["code_symbols"]
        code_colors = app_config.ui["code_colors"]
        code_style = app_config.ui["code_style"]

        options = zip(
            [
                Text(code_symbol, style=f"{code_color} {code_style}")
                for code_symbol, code_color in zip(code_symbols, code_colors)
            ],
            range(app_config.current_variation["num_symbols"]),
        )

        yield Select(
            options=options,
            prompt=app_config.ui["code_blank_symbol"],
        )

        # yield Button("Check", flat=True)
