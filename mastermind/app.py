import tomllib
from pathlib import Path

from textual.app import App, ComposeResult
from textual.containers import Horizontal, VerticalScroll
from textual.widgets import Button, Footer, Header, Select, Static


class MastermindApp(App):
    TITLE = "Mastermind"

    CSS_PATH = "styles.tcss"

    def __init__(self) -> None:
        super().__init__()

        with open(Path(__file__).parent / "config.toml", mode="rb") as toml:
            self.config = tomllib.load(toml)

        self.board: VerticalScroll = VerticalScroll(id="board")

        self.color_pegs: list[Select]

    def compose(self) -> ComposeResult:
        yield Header(icon="❔")

        # yield Horizontal(
        #     Static("01", classes="num"),
        #     Static("🔵", classes="static_color_peg"),
        #     Static("🔴", classes="static_color_peg"),
        #     Static("🟢", classes="static_color_peg"),
        #     Static("🟣", classes="static_color_peg"),
        #     Static("🔴 ⚪ ⭕ ⭕", classes="feedback_pegs"),
        #     classes="row",
        # )

        yield self.board
        yield Footer()

    def new_game(self) -> None:
        self.color_pegs = [
            Select(
                options=zip(self.config["pegs"]["color_pegs"], range(1, 9)),
                prompt=self.config["pegs"]["hole"],
                classes="color_peg",
            )
            for _ in range(4)
        ]

        horizontal = Horizontal(
            Static("01", classes="num"),
            *self.color_pegs,
            Button("❔", classes="check"),
            classes="row",
        )

        self.board.mount(horizontal)

        # horizontal = Horizontal(classes="row")
        # self.board.mount(horizontal)

        # horizontal.mount()

        # for widget in self.row:
        #     horizontal.mount(widget)

        # horizontal.mount()

    def on_mount(self) -> None:
        self.new_game()
