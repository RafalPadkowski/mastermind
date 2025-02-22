import dataclasses
from typing import Any

from textual import work
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.widgets import Button, Footer, Header, Select, Switch
from textual_utils import (
    AboutHeaderIcon,
    ConfirmScreen,
    SettingRow,
    SettingsScreen,
    _,
    init_translation,
    load_settings,
    mount_about_header_icon,
    save_settings,
    set_translation,
)

from mastermind.constants import (
    APP_METADATA,
    ICON,
    KEY_TO_BINDING,
    LOCALEDIR,
    SETTINGS_PATH,
)
from mastermind.settings import LANGUAGES, VARIATIONS, app_settings
from mastermind.widgets.board import Board


class MastermindApp(App):
    TITLE = "Master Mind"
    CSS_PATH = "styles.tcss"
    ENABLE_COMMAND_PALETTE = False
    BINDINGS = list(KEY_TO_BINDING.values())

    def __init__(self) -> None:
        super().__init__()

        settings_dict: dict[str, Any] = load_settings(SETTINGS_PATH)
        app_settings.set(settings_dict)

        init_translation(LOCALEDIR)
        set_translation(app_settings.language)
        self.translate_bindings()

        self.board: Board = Board()

    def compose(self) -> ComposeResult:
        yield Header()
        yield self.board
        yield Footer()

    async def on_mount(self) -> None:
        await mount_about_header_icon(
            current_app=self,
            icon=ICON,
            app_metadata=APP_METADATA,
        )

        self.translate_about_header_icon()

    def translate_bindings(self) -> None:
        for key, binding in KEY_TO_BINDING.items():
            current_binding: Binding = self._bindings.key_to_bindings[key][0]
            self._bindings.key_to_bindings[key] = [
                dataclasses.replace(current_binding, description=_(binding.description))
            ]

    def translate_about_header_icon(self) -> None:
        about_header_icon: AboutHeaderIcon = self.query_one(AboutHeaderIcon)
        about_header_icon.tooltip = _("About")

    def translate(self) -> None:
        self.translate_bindings()
        self.translate_about_header_icon()

    def on_button_pressed(self, message: Button.Pressed):
        if message.button.id != "check":
            return

        message.button.remove()

        self.board.current_row.disabled = True

        for code_peg in self.board.current_row.code_pegs:
            code_peg.children[0].children[1].remove()

        if self.board.current_row_number < app_settings.variation.num_rows:
            self.board.add_row()
        else:
            self.notify("Koniec", timeout=2)

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
            self.board = Board()
            self.mount(self.board)

    @work
    async def action_settings(self) -> None:
        setting_rows: dict[str, SettingRow] = {
            key: value
            for key, value in zip(
                app_settings.__dict__.keys(),
                [
                    SettingRow(
                        label="Language:",
                        widget=Select(
                            options=zip(
                                [_(value) for value in LANGUAGES.values()],
                                LANGUAGES.keys(),
                            ),
                            value=app_settings.language,
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
                            value=app_settings.variation.name,
                            allow_blank=False,
                        ),
                    ),
                    SettingRow(
                        label="Duplicate colors:",
                        widget=Switch(value=app_settings.duplicate_colors),
                    ),
                    SettingRow(
                        label="Blank color:",
                        widget=Switch(value=app_settings.blank_color),
                    ),
                ],
            )
        }

        settings_dict = await self.push_screen_wait(
            SettingsScreen(
                dialog_title="Settings",
                dialog_subtitle=APP_METADATA.name,
                setting_rows=setting_rows,
            )
        )

        if settings_dict is not None:
            old_language = app_settings.language

            app_settings.set(settings_dict)

            if old_language != app_settings.language:
                set_translation(app_settings.language)
                self.translate()

            save_settings(settings_dict, SETTINGS_PATH)
