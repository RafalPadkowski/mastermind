import dataclasses
from typing import Any

from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Horizontal, VerticalScroll
from textual.widgets import Button, Footer, Header, Label, Select
from textual.widgets._header import HeaderIcon

from mastermind.constants import (
    BLANK_COLOR,
    CODE_PEG_COLORS,
    ICON,
    KEY_TO_BINDING,
    SETTINGS_PATH,
)
from mastermind.header_icon import MastermindHeaderIcon
from mastermind.i18n import _, set_translation
from mastermind.screens import SettingsScreen
from mastermind.settings import Settings, load_settings, parse_settings, save_settings

__author__ = "Rafal Padkowski"
__version__ = "2.0"
__email__ = "rafaelp@poczta.onet.pl"


class MastermindApp(App):
    TITLE = "Master Mind"

    CSS_PATH = "styles.tcss"

    BINDINGS = list(KEY_TO_BINDING.values())

    ENABLE_COMMAND_PALETTE = False

    def __init__(self) -> None:
        super().__init__()

        settings_dict: dict[str, Any] = load_settings(SETTINGS_PATH)
        self.settings: Settings = parse_settings(settings_dict)

        self.board: VerticalScroll
        self.code_pegs: list[Select]

    def compose(self) -> ComposeResult:
        yield Header(icon=ICON)

        self.board = VerticalScroll()
        yield self.board

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

    async def on_mount(self) -> None:
        # print("--- MOUNT ---")
        header_icon = self.query_one(HeaderIcon)
        header_icon.remove()

        header = self.query_one(Header)
        header_icon = MastermindHeaderIcon()
        await header.mount(header_icon)
        header_icon.icon = ICON

        self.translate()

        self.mount(Footer())

        self.create_new_game()

    def translate(self) -> None:
        set_translation(self.settings.language)

        header_icon: MastermindHeaderIcon = self.query_one(MastermindHeaderIcon)
        header_icon.tooltip = _("About")

        for key, binding in KEY_TO_BINDING.items():
            current_binding: Binding = self._bindings.key_to_bindings[key][0]
            self._bindings.key_to_bindings[key] = [
                dataclasses.replace(current_binding, description=_(binding.description))
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
