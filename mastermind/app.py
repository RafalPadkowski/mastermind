from textual.app import App, ComposeResult
from textual.containers import Horizontal, VerticalScroll
from textual.widgets import Button, Footer, Header, Label, Select

from mastermind.constants import BLANK_COLOR, CODE_PEG_COLORS, ICON, SETTINGS_PATH
from mastermind.screens import SettingsScreen
from mastermind.settings import load_settings


class MastermindApp(App):
    TITLE = "Mastermind"
    CSS_PATH = "styles.tcss"
    BINDINGS = [
        ("s", "settings", "Settings"),
    ]

    def __init__(self) -> None:
        super().__init__()

        self.settings = load_settings(SETTINGS_PATH)

        self.board: VerticalScroll
        self.code_pegs: list[Select]

    def compose(self) -> ComposeResult:
        yield Header(icon=ICON)

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

        print("--- COMPOSE ---")

    def on_mount(self) -> None:
        print("--- MOUNT ---")
        self.create_new_game()

    def create_new_game(self) -> None:
        self.create_code_pegs()

        row = Horizontal(
            Label("01", classes="num"),
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
                options=zip(CODE_PEG_COLORS, range(1, num_colors + 1)),
                prompt=BLANK_COLOR,
                classes="code_peg",
            )
            for _ in range(num_pegs)
        ]

    def action_settings(self) -> None:
        self.push_screen(SettingsScreen())
