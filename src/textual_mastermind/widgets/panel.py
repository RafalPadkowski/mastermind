from rich.text import Text
from textual.app import ComposeResult
from textual.containers import Horizontal, VerticalScroll
from textual.widgets import Button, Select

from ..app_config import app_config


class Panel(VerticalScroll):
    def __init__(self) -> None:
        super().__init__()

    def compose(self) -> ComposeResult:
        code_letters = app_config.ui["code_letters"]
        code_colors = app_config.ui["code_colors"]
        code_style = app_config.ui["code_style"]

        options = zip(
            [
                Text(code_letter, style=f"{code_color} {code_style}")
                for code_letter, code_color in zip(code_letters, code_colors)
            ],
            range(app_config.current_variation["num_colors"]),
        )

        yield Select(
            options=options,
            prompt=app_config.ui["code_blank_letter"],
        )

        # yield Button("Check", flat=True)
