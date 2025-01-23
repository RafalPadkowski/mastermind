from typing import TYPE_CHECKING, Any, cast

from textual.app import ComposeResult
from textual.containers import Grid
from textual.screen import ModalScreen
from textual.widgets import Button, Header, Label, Select, Switch

from mastermind.constants import ICON, LANGUAGES, VARIATIONS

if TYPE_CHECKING:
    from mastermind.app import MastermindApp


class SettingsScreen(ModalScreen[dict[str, Any] | None]):
    def __init__(self) -> None:
        super().__init__()

        self.language_select: Select[str]
        self.variation_select: Select[str]
        self.duplicate_colors_switch: Switch
        self.blank_color_switch: Switch

    def compose(self) -> ComposeResult:
        app = cast("MastermindApp", self.app)

        self.language_select = Select(
            options=zip(LANGUAGES.values(), LANGUAGES.keys()),
            value=app.settings.language,
            allow_blank=False,
        )

        self.variation_select = Select(
            options=zip(
                [variation.description for variation in VARIATIONS.values()],
                VARIATIONS.keys(),
            ),
            value=app.settings.variation.name,
            allow_blank=False,
        )

        self.duplicate_colors_switch = Switch(value=app.settings.duplicate_colors)

        self.blank_color_switch = Switch(value=app.settings.blank_color)

        self.dialog = Grid(
            Label("\nLanguage:"),
            self.language_select,
            Label("\nVariation:"),
            self.variation_select,
            Label("\nKolory mogą się powtarzać:"),
            self.duplicate_colors_switch,
            Label("\nPuste miejsce jako dodatkowy kolor:"),
            self.blank_color_switch,
            Button("Save", variant="primary", id="save"),
            Button("Cancel", variant="error", id="cancel"),
            id="settings_dialog",
        )

        yield Header(icon=ICON)
        yield self.dialog

    def on_mount(self) -> None:
        self.dialog.border_title = "Settings"

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "save":
            settings_dict: dict[str, Any] = dict(
                language=self.language_select.value,
                variation=self.variation_select.value,
                duplicate_colors=self.duplicate_colors_switch.value,
                blank_color=self.blank_color_switch.value,
            )
            self.dismiss(settings_dict)
        else:
            self.dismiss(None)
