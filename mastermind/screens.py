from typing import TYPE_CHECKING, Any, cast

from rich.text import Text
from textual.app import ComposeResult
from textual.containers import Grid
from textual.screen import ModalScreen
from textual.widgets import Button, Label, Link, Select, Switch
from textual_utils import AppMetadata, _

from mastermind.constants import LANGUAGES, VARIATIONS

if TYPE_CHECKING:
    from mastermind.app import MastermindApp


class AboutScreen(ModalScreen):
    CSS_PATH = ["screens.tcss", "about_screen.tcss"]

    def __init__(self, app_metadata: AppMetadata) -> None:
        super().__init__()

        self.app_metadata = app_metadata

    def compose(self) -> ComposeResult:
        app_name = (
            f"{self.app_metadata.name} {self.app_metadata.version}"
            f"  {self.app_metadata.codename}"
        )

        self.dialog = Grid(
            Label(Text(app_name, style="bold green")),
            Label(_(self.app_metadata.author)),
            Link(self.app_metadata.email, url=f"mailto:{self.app_metadata.email}"),
            Button("Ok", variant="primary", id="ok"),
            id="about_dialog",
        )

        yield self.dialog

    def on_mount(self) -> None:
        self.dialog.border_subtitle = self.app_metadata.name
        self.dialog.border_title = _("About")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "ok":
            self.app.pop_screen()


class ConfirmScreen(ModalScreen[bool]):
    CSS_PATH = ["screens.tcss", "confirm_screen.tcss"]

    def compose(self) -> ComposeResult:
        self.dialog = Grid(
            Label(_("Are you sure you want to start a new game?"), id="question"),
            Button(_("Yes"), variant="primary", id="yes"),
            Button(_("No"), variant="error", id="no"),
            id="confirm_dialog",
        )

        yield self.dialog

    def on_mount(self) -> None:
        self.dialog.border_subtitle = "Master Mind"
        self.dialog.border_title = _("New game")

        self.dialog.styles.grid_columns = "20"

        # self.query_one("#no", Button).focus()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "yes":
            self.dismiss(True)
        else:
            self.dismiss(False)


class SettingsScreen(ModalScreen[dict[str, Any] | None]):
    CSS_PATH = ["screens.tcss", "settings_screen.tcss"]

    def __init__(self) -> None:
        super().__init__()

        self.language_select: Select[str]
        self.variation_select: Select[str]
        self.duplicate_colors_switch: Switch
        self.blank_color_switch: Switch

    def compose(self) -> ComposeResult:
        app = cast("MastermindApp", self.app)

        self.language_select = Select(
            options=zip([_(value) for value in LANGUAGES.values()], LANGUAGES.keys()),
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
            Label(_("Language:")),
            self.language_select,
            Label(_("Variation:")),
            self.variation_select,
            Label(_("Duplicate colors:")),
            self.duplicate_colors_switch,
            Label(_("Blank color:")),
            self.blank_color_switch,
            Button(_("Save"), variant="primary", id="save"),
            Button(_("Cancel"), variant="error", id="cancel"),
            id="settings_dialog",
        )

        yield self.dialog

    def on_mount(self) -> None:
        self.dialog.border_subtitle = "Master Mind"
        self.dialog.border_title = _("Settings")

        self.dialog.styles.width = 110
        self.dialog.styles.grid_columns = "48"

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "save":
            settings_dict: dict[str, Any] = dict(
                language=self.language_select.value,
                variation=self.variation_select.value,
                duplicate_colors=self.duplicate_colors_switch.value,
                blank_color=self.blank_color_switch.value,
            )
            print(settings_dict)
            self.dismiss(settings_dict)
        else:
            self.dismiss(None)
