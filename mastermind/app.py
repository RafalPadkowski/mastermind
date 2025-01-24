import dataclasses
from typing import Any

from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Horizontal, VerticalScroll
from textual.widgets import Button, Footer, Header, Label, Select
from textual.widgets._header import HeaderIcon

from mastermind.constants import (
    BINDING_DESCRIPTIONS,
    BLANK_COLOR,
    CODE_PEG_COLORS,
    ICON,
    SETTINGS_PATH,
)
from mastermind.i18n import _, set_translation
from mastermind.screens import SettingsScreen
from mastermind.settings import Settings, load_settings, parse_settings, save_settings


class MastermindApp(App):
    TITLE = "Master Mind"

    CSS_PATH = "styles.tcss"

    BINDINGS = [
        ("f2", "new_game", "New game"),
        ("f3", "settings", "Settings"),
    ]
    ENABLE_COMMAND_PALETTE = False

    def __init__(self) -> None:
        super().__init__()

        settings_dict: dict[str, Any] = load_settings(SETTINGS_PATH)
        self.settings: Settings = parse_settings(settings_dict)

        self.translate()

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

        # print("--- COMPOSE ---")

    def on_mount(self) -> None:
        # print("--- MOUNT ---")
        self.query_one(HeaderIcon).tooltip = None

        self.create_new_game()

    def get_key_display(self, binding: Binding) -> str:
        return binding.key.upper()

    def action_help_quit(self) -> None:
        """Bound to ctrl+C to alert the user that it no longer quits."""
        # Doing this because users will reflexively hit ctrl+C to exit
        # Ctrl+C is now bound to copy if an input / textarea is focused.
        # This makes is possible, even likely, that a user may do it accidentally
        # -- which would be maddening.
        # Rather than do nothing, we can make an educated guess the user was trying
        # to quit, and inform them how you really quit.
        for key, active_binding in self.active_bindings.items():
            if active_binding.binding.action in ("quit", "app.quit"):
                # self.notify(
                #     f"Press [b]{key}[/b] to quit the app",
                #     title="Do you want to quit?"
                # )
                self.notify(
                    f"{_("Press")} [b]{key}[/b] {_("to quit the app")}",
                    title=_("Do you want to quit?"),
                )
                return

    def translate(self) -> None:
        set_translation(self.settings.language)

        for key, description in BINDING_DESCRIPTIONS.items():
            binding: Binding = self._bindings.key_to_bindings[key][0]
            self._bindings.key_to_bindings[key] = [
                dataclasses.replace(binding, description=_(description))
            ]

    def create_new_game(self) -> None:
        self.create_code_pegs()

        row: Horizontal = Horizontal(
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
        self.push_screen(SettingsScreen(), callback=self.check_settings)

    def check_settings(self, settings_dict: dict[str, Any] | None) -> None:
        if settings_dict is not None:
            self.settings = parse_settings(settings_dict)
            self.translate()
            save_settings(settings_dict, SETTINGS_PATH)
