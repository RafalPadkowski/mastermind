from rich.text import Text
from textual.app import ComposeResult
from textual.containers import Vertical
from textual.widgets import Select

from ..app_config import app_config


class Panel(Vertical):
    def __init__(self) -> None:
        super().__init__()

        self.select: Select

    def compose(self) -> ComposeResult:
        letters = [app_config.ui["code_blank_letter"]] + app_config.ui["code_letters"]
        colors = ["$text"] + app_config.ui["code_colors"]
        style = app_config.ui["code_style"]

        options = zip(
            [
                Text(letter, style=f"{color} {style}")
                for letter, color in zip(letters, colors)
            ],
            range(app_config.current_variation["num_colors"] + 1),
        )

        self.select = Select(options, allow_blank=False)
        yield self.select
