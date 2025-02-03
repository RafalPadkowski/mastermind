import dataclasses
from typing import Any

from textual import work
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Horizontal, VerticalScroll
from textual.widgets import Button, Footer, Header, Label, Select, Switch
from textual_utils import (
    AboutHeaderIcon,
    ConfirmScreen,
    SettingRow,
    SettingsScreen,
    _,
    init_translation,
    mount_about_header_icon,
    set_translation,
)

from mastermind.constants import (
    APP_METADATA,
    BLANK_COLOR,
    CODE_PEG_COLORS,
    ICON,
    KEY_TO_BINDING,
    LANGUAGES,
    LOCALEDIR,
    SETTINGS_DIALOG_WIDTH,
    SETTINGS_PATH,
    VARIATIONS,
)
from mastermind.settings import Settings, load_settings, parse_settings, save_settings


class MastermindApp(App):
    TITLE = "Master Mind"

    CSS_PATH = "styles.tcss"

    BINDINGS = list(KEY_TO_BINDING.values())

    ENABLE_COMMAND_PALETTE = False

    def __init__(self) -> None:
        super().__init__()

        init_translation(LOCALEDIR)

        settings_dict: dict[str, Any] = load_settings(SETTINGS_PATH)
        self.settings: Settings = parse_settings(settings_dict)

        self.board: VerticalScroll = VerticalScroll()

        self.row_number: int
        self.code_pegs: list[Select]

    def compose(self) -> ComposeResult:
        yield Header()

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
        await mount_about_header_icon(
            current_app=self,
            icon=ICON,
            app_metadata=APP_METADATA,
        )

        self.translate()

        self.mount(self.board)
        self.create_new_game()

        self.mount(Footer())

    def translate(self) -> None:
        set_translation(self.settings.language)

        about_header_icon: AboutHeaderIcon = self.query_one(AboutHeaderIcon)
        about_header_icon.tooltip = _("About")

        for key, binding in KEY_TO_BINDING.items():
            current_binding: Binding = self._bindings.key_to_bindings[key][0]
            self._bindings.key_to_bindings[key] = [
                dataclasses.replace(current_binding, description=_(binding.description))
            ]

    @work
    async def action_new_game(self) -> None:
        if await self.push_screen_wait(
            ConfirmScreen(
                dialog_title="New game",
                dialog_subtitle=APP_METADATA.name,
                question="Are you sure you want to start a new game?",
            )
        ):
            self.board.remove()
            self.board = VerticalScroll()
            self.mount(self.board)

            self.create_new_game()

    def create_new_game(self) -> None:
        self.row_number = 1

        self.create_new_row()

    def create_new_row(self) -> None:
        self.create_code_pegs()

        row: Horizontal = Horizontal(
            Label(f"{self.row_number:02}", classes="num"),
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

    @work
    async def action_settings(self) -> None:
        setting_rows: dict[str, SettingRow] = {
            key: value
            for key, value in zip(
                self.settings.__dict__.keys(),
                [
                    SettingRow(
                        label="Language:",
                        widget=Select(
                            options=zip(
                                [_(value) for value in LANGUAGES.values()],
                                LANGUAGES.keys(),
                            ),
                            value=self.settings.language,
                            allow_blank=False,
                        ),
                    ),
                    SettingRow(
                        label="Variation:",
                        widget=Select(
                            options=zip(
                                [
                                    variation.description
                                    for variation in VARIATIONS.values()
                                ],
                                VARIATIONS.keys(),
                            ),
                            value=self.settings.variation.name,
                            allow_blank=False,
                        ),
                    ),
                    SettingRow(
                        label="Duplicate colors:",
                        widget=Switch(value=self.settings.duplicate_colors),
                    ),
                    SettingRow(
                        label="Blank color:",
                        widget=Switch(value=self.settings.blank_color),
                    ),
                ],
            )
        }

        settings_dict = await self.push_screen_wait(
            SettingsScreen(
                dialog_title="Settings",
                dialog_subtitle=APP_METADATA.name,
                dialog_width=SETTINGS_DIALOG_WIDTH,
                setting_rows=setting_rows,
            )
        )

        if settings_dict is not None:
            self.settings = parse_settings(settings_dict)
            self.translate()
            save_settings(settings_dict, SETTINGS_PATH)
