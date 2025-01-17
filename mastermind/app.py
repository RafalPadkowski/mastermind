import tomllib
from pathlib import Path

from textual.app import App, ComposeResult
from textual.containers import Horizontal, VerticalScroll
from textual.widgets import Button, Footer, Header, Select, Static

from mastermind.settings import Settings


class MastermindApp(App):
    TITLE = "Mastermind"

    CSS_PATH = "styles.tcss"

    def __init__(self) -> None:
        super().__init__()

        with open(Path(__file__).parent / "config.toml", mode="rb") as toml:
            self.config = tomllib.load(toml)

        variation = self.config["settings"]["variation"]

        self.settings = Settings(
            self.config["variations"][variation]["num_rows"],
            self.config["variations"][variation]["num_pegs"],
            self.config["variations"][variation]["num_colors"],
            self.config["settings"]["blank_color"],
            self.config["settings"]["duplicate_colors"],
        )

        self.board: VerticalScroll
        self.code_pegs: list[Select]

    def compose(self) -> ComposeResult:
        yield Header(icon=self.config["general"]["icon"])

        self.board = VerticalScroll()
        yield self.board

        yield Footer()

        # yield Horizontal(
        #     Static("01", classes="num"),
        #     Static("🔵", classes="static_color_peg"),
        #     Static("🔴", classes="static_color_peg"),
        #     Static("🟢", classes="static_color_peg"),
        #     Static("🟣", classes="static_color_peg"),
        #     Static("🔴 ⚪ ⭕ ⭕", classes="feedback_pegs"),
        #     classes="row",
        # )

    def on_mount(self) -> None:
        self.create_new_game()

    def create_new_game(self) -> None:
        self.create_code_pegs()

        row = Horizontal(
            Static("01", classes="num"),
            *self.code_pegs,
            Button("❔", classes="check"),
            classes="row",
        )

        self.board.mount(row)

    def create_code_pegs(self) -> None:
        num_pegs = self.settings.num_pegs
        num_colors = self.settings.num_colors

        self.code_pegs = [
            Select(
                options=zip(
                    self.config["colors"]["code_peg_colors"], range(1, num_colors + 1)
                ),
                prompt=self.config["colors"]["blank_color"],
                classes="code_peg",
            )
            for _ in range(num_pegs)
        ]
