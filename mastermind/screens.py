from textual.app import ComposeResult
from textual.containers import Grid
from textual.screen import ModalScreen
from textual.widgets import Button, Label, Select, Switch


class SettingsScreen(ModalScreen):
    def compose(self) -> ComposeResult:
        self.dialog = Grid(
            Label("Variation:"),
            Select(
                options=[
                    ("mini (6 rows, 4 pegs, 6 colors)", 1),
                    ("original (10 rows, 4 pegs, 6 colors)", 2),
                    ("super (12 rows, 5 pegs, 8 colors)", 3),
                ],
                allow_blank=False,
            ),
            Label("Blank color:"),
            Switch(value=False),
            Label("Duplicate colors:"),
            Switch(value=False),
            Button("Save", variant="primary", id="save"),
            Button("Cancel", variant="error", id="cancel"),
            id="settings_dialog",
        )

        yield self.dialog

    def on_mount(self) -> None:
        self.dialog.border_title = "Settings"

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "quit":
            self.app.exit()
        else:
            self.app.pop_screen()
