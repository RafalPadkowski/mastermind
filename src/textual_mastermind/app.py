from dataclasses import dataclass, field, replace
from importlib.metadata import metadata
from typing import cast

from config import Config
from config.settings import SettingBoolean, SettingOption, SettingOptions
from i18n import tr
from textual import work
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.events import Click
from textual.widget import Widget
from textual.widgets import Footer, Header, Label, Select, Switch
from textual_utils import (
    AboutHeaderIcon,
    AppMetadata,
    ConfirmScreen,
    SettingsScreen,
    mount_about_header_icon,
)

from .constants import (
    BLANK_COLOR,
    CODE_PEG_COLORS,
    FEEDBACK_PEG_COLORS,
    KEY_TO_BINDING,
    LOCALEDIR,
    SETTINGS_PATH,
)

# from .game import Game
from .settings import variations

# from .widgets.board import Board


class MastermindApp(App[None]):
    CSS_PATH = "styles.tcss"
    ENABLE_COMMAND_PALETTE = False
    BINDINGS = list(KEY_TO_BINDING.values())

    def __init__(self) -> None:
        super().__init__()

        @dataclass
        class AppUi:
            icon: str = field(init=False)

        @dataclass
        class AppSettings:
            language: SettingOptions
            variation: SettingOptions
            duplicate_colors: SettingBoolean
            blank_color: SettingBoolean

        class AppConfig(Config[AppUi, AppSettings]):
            ui: AppUi
            settings: AppSettings

        self.config = AppConfig(
            ui=AppUi(),
            settings=AppSettings(
                language=SettingOptions(
                    label="Language:",
                    default_value="en",
                    options=[
                        SettingOption(display_str="English", value="en"),
                        SettingOption(display_str="Polish", value="pl"),
                    ],
                ),
                variation=SettingOptions(
                    label="Variation:",
                    default_value="original",
                    options=[
                        SettingOption(v.description, k) for k, v in variations.items()
                    ],
                ),
                duplicate_colors=SettingBoolean(
                    label="Duplicate colors:",
                    default_value=False,
                ),
                blank_color=SettingBoolean(
                    label="Blank color:",
                    default_value=False,
                ),
            ),
        )

        pkg_name = cast(str, __package__)
        pkg_metadata = metadata(pkg_name)

        self.app_metadata = AppMetadata(
            name="Mastermind",
            version=pkg_metadata["Version"],
            icon=self.config.ui.icon,
            description="Break the hidden code",
            author=pkg_metadata["Author"],
            email=pkg_metadata["Author-email"].split("<")[1][:-1],
        )

        tr.localedir = LOCALEDIR
        tr.language = self.config.settings.language.current_value

        self.translate_bindings()

        # self.board: Board
        # self.game: Game

    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()

    async def on_mount(self) -> None:
        await mount_about_header_icon(
            current_app=self,
            app_metadata=self.app_metadata,
        )
        self.translate_about_header_icon()

        self.title = self.app_metadata.name

        # self.create_new_game()

    def translate_bindings(self) -> None:
        for key, binding in KEY_TO_BINDING.items():
            current_binding: Binding = self._bindings.key_to_bindings[key][0]
            self._bindings.key_to_bindings[key] = [
                replace(current_binding, description=tr(binding.description))
            ]

    def translate_about_header_icon(self) -> None:
        about_header_icon: AboutHeaderIcon = self.query_one(AboutHeaderIcon)
        about_header_icon.tooltip = tr("About")

    def translate(self) -> None:
        self.translate_bindings()
        self.translate_about_header_icon()

    def create_new_game(self):
        if hasattr(self, "game"):
            self.board.remove()

        self.game = Game()

        self.board = Board(self.game)
        self.mount(self.board)

    async def on_click(self, event: Click) -> None:
        if isinstance(event.widget, Widget):
            if event.widget.id == "check":
                await self.on_click_check()

    async def on_click_check(self) -> None:
        code_peg_values: list[int] = []
        for code_peg in self.board.current_row.code_pegs:
            code_peg.query_one("SelectCurrent Static.down-arrow").remove()

            code_peg_value: int
            if isinstance(code_peg.value, int):
                code_peg_value = code_peg.value
            else:
                code_peg_value = 0

            code_peg_values.append(code_peg_value)

        num_red_pegs: int
        num_white_pegs: int
        num_red_pegs, num_white_pegs = await self.game.check_code(
            breaker_code=code_peg_values
        )

        self.board.current_row.query_one("#check").remove()

        self.board.current_row.mount(
            Label(
                "".join(
                    [
                        (FEEDBACK_PEG_COLORS[0] + " ") * num_red_pegs,
                        (FEEDBACK_PEG_COLORS[1] + " ") * num_white_pegs,
                        (BLANK_COLOR + " ")
                        * (self.game.num_pegs - num_red_pegs - num_white_pegs),
                    ]
                ),
                classes="feedback_pegs",
            )
        )

        self.board.current_row.disabled = True

        if num_red_pegs == self.game.num_pegs:
            self.notify(_("Congratulations!"))
        else:
            if self.board.current_row_number < self.game.num_rows:
                self.board.add_row()
            else:
                maker_code: list[int] = self.game.get_maker_code()
                maker_code_str: str = ""
                for color in maker_code:
                    if color == 0:
                        maker_code_str += BLANK_COLOR + " "
                    else:
                        maker_code_str += CODE_PEG_COLORS[color - 1] + " "

                self.notify(
                    f"{_('Better luck next time')}\n{_('Code')}: {maker_code_str}",
                    timeout=30,
                )

    @work
    async def action_new_game(self) -> None:
        if await self.push_screen_wait(
            ConfirmScreen(
                dialog_title="New game",
                dialog_subtitle=APP_METADATA.name,
                question="Are you sure you want to start a new game?",
            )
        ):
            self.create_new_game()

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

            old_variation = app_settings.variation
            old_duplicate_colors = app_settings.duplicate_colors
            old_blank_color = app_settings.blank_color

            app_settings.set(settings_dict)

            if old_language != app_settings.language:
                set_translation(app_settings.language)
                self.translate()

            if (
                old_variation.name != app_settings.variation.name
                or old_duplicate_colors != app_settings.duplicate_colors
                or old_blank_color != app_settings.blank_color
            ):
                self.notify(
                    _("New game settings will be applied to a new game"), timeout=5
                )

            save_settings(settings_dict, SETTINGS_PATH)
