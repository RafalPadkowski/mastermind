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

        self.color_pegs: list[str] = self.config["pegs"]["color_pegs"]
        self.hole: str = self.config["pegs"]["hole"]

        self.row: list[Select] = [
            Select(
                options=zip(self.color_pegs, range(1, 9)),
                prompt=self.hole,
                classes="color_peg",
            )
            for _ in range(4)
        ]

    def compose(self) -> ComposeResult:
        yield Header(icon="❔")

        # yield Horizontal(
        #     Static("01", classes="num"),
        #     Static("🔵", classes="static_color_peg"),
        #     Static("🔴", classes="static_color_peg"),
        #     Static("🟢", classes="static_color_peg"),
        #     Static("🟣", classes="static_color_peg"),
        #     Static("🔴 ⚪ ⭕ ⭕", classes="feedback"),
        #     classes="row",
        # )

        yield self.board
        yield Footer()

    def new_game(self) -> None:
        # with Horizontal(classes="row"):
        #     yield Static("02", classes="num")

        #     for widget in self.row:
        #         yield widget

        #     yield Button("❔", classes="check")

        horizontal = Horizontal(
            Static("01", classes="num"),
            *self.row,
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
