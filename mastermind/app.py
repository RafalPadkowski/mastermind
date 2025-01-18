from textual.app import App, ComposeResult
from textual.containers import Horizontal, VerticalScroll
from textual.widgets import Button, Footer, Header, Select, Static

from mastermind.config import app_config
from mastermind.settings import app_settings


class MastermindApp(App):
    TITLE = "Mastermind"

    CSS_PATH = "styles.tcss"

    def __init__(self) -> None:
        super().__init__()

        self.config = app_config
        self.settings = app_settings

        self.board: VerticalScroll
        self.code_pegs: list[Select]

    def compose(self) -> ComposeResult:
        yield Header(icon=self.config.general.icon)

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
        num_pegs: int = self.settings.variation.num_pegs
        num_colors: int = self.settings.variation.num_colors

        self.code_pegs = [
            Select(
                options=zip(
                    self.config.colors.code_peg_colors, range(1, num_colors + 1)
                ),
                prompt=self.config.colors.blank_color,
                classes="code_peg",
            )
            for _ in range(num_pegs)
        ]
