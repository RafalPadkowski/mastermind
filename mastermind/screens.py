from textual.app import ComposeResult
from textual.containers import Grid
from textual.screen import ModalScreen
from textual.widgets import Button, Label


class SettingsScreen(ModalScreen):
    def compose(self) -> ComposeResult:
        yield Grid(
            # Label("Are you sure you want to quit?", id="question"),
            Button("Save", variant="error", id="quit"),
            Button("Cancel", variant="primary", id="cancel"),
            id="settings_dialog",
        )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "quit":
            self.app.exit()
        else:
            self.app.pop_screen()
