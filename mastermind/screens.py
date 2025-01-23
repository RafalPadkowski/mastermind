from typing import TYPE_CHECKING, cast

from textual.app import ComposeResult
from textual.containers import Grid
from textual.screen import ModalScreen
from textual.widgets import Button, Header, Label, Select, Switch

from mastermind.constants import ICON, LANGUAGES, VARIATIONS

if TYPE_CHECKING:
    from mastermind.app import MastermindApp


class SettingsScreen(ModalScreen):
    def compose(self) -> ComposeResult:
        app = cast("MastermindApp", self.app)

        self.dialog = Grid(
            Label("\nLanguage:"),
            Select(
                options=zip(LANGUAGES.values(), range(len(LANGUAGES))),
                value=list(LANGUAGES.keys()).index(app.settings.language),
                allow_blank=False,
            ),
            Label("\nVariation:"),
            Select(
                options=zip(
                    [variation.description for variation in VARIATIONS.values()],
                    range(len(VARIATIONS)),
                ),
                value=list(VARIATIONS.keys()).index(app.settings.variation.name),
                allow_blank=False,
            ),
            Label("\nKolory mogą się powtarzać:"),
            Switch(value=False),
            Label("\nPuste miejsce jako dodatkowy kolor:"),
            Switch(value=False),
            Button("Save", variant="primary", id="save"),
            Button("Cancel", variant="error", id="cancel"),
            id="settings_dialog",
        )

        yield Header(icon=ICON)
        yield self.dialog

    def on_mount(self) -> None:
        self.dialog.border_title = "Settings"

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "quit":
            self.app.exit()
        else:
            self.app.pop_screen()
