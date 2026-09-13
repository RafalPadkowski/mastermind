from textual.app import ComposeResult
from textual.containers import Horizontal, VerticalScroll
from textual.widgets import Button, Select

from ..app_config import app_config


class Panel(VerticalScroll):
    def __init__(self) -> None:
        super().__init__()

    def compose(self) -> ComposeResult:
        current_variation = app_config.current_variation

        code_symbols = app_config.ui["code_symbols"]
        num_symbols = current_variation["num_symbols"]

        with Horizontal():
            for _ in range(current_variation["num_pegs"]):
                yield Select(
                    options=zip(code_symbols[:num_symbols], range(num_symbols)),
                    prompt=app_config.ui["code_blank_symbol"],
                )

        yield Button("Check")
