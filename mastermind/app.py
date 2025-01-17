import tomllib
from pathlib import Path

from textual.app import App, ComposeResult
from textual.containers import Horizontal
from textual.widgets import Button, Footer, Header, Select, Static


class MastermindApp(App):
    TITLE = "Mastermind"

    CSS_PATH = "styles.tcss"

    def __init__(self) -> None:
        super().__init__()

        with open(Path("mastermind") / "config.toml", mode="rb") as toml:
            self.config = tomllib.load(toml)

        self.code_pegs: list[str] = self.config["pegs"]["code_pegs"]
        self.hole: str = self.config["pegs"]["hole"]

        self.row: list[Select] = [
            Select(
                options=zip(self.code_pegs, range(1, 9)),
                prompt=self.hole,
                classes="color_peg",
            )
            for _ in range(4)
        ]

    def compose(self) -> ComposeResult:
        yield Header(icon="❔")

        yield Horizontal(
            Static("01", classes="num"),
            Static("🔵", classes="static_color_peg"),
            Static("🔴", classes="static_color_peg"),
            Static("🟢", classes="static_color_peg"),
            Static("🟣", classes="static_color_peg"),
            Static("🔴 ⚪ ⭕ ⭕", classes="feedback"),
            classes="row",
        )

        with Horizontal(classes="row"):
            yield Static("02", classes="num")

            for widget in self.row:
                yield widget

            yield Button("❔", classes="check")

        yield Footer()
