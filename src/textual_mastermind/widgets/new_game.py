from textual.app import ComposeResult
from textual.screen import ModalScreen
from textual.widgets import Checkbox, Footer, Header, Label, RadioButton, RadioSet
from tilsit_i18n import tr

from ..app_config import app_config
from ..bindings import NEW_GAME_BINDINGS

BORDER_WIDTH = 1
RADIO_SET_LEFT_PADDING_WIDTH = 5
RADIO_SET_RIGHT_PADDING_WIDTH = 2


class NewGameScreen(ModalScreen[bool]):
    BINDINGS = NEW_GAME_BINDINGS

    def compose(self) -> ComposeResult:
        yield Header(icon=app_config.ui["new_game_icon"])

        self.variation_radio_buttons = {
            name: RadioButton(
                label=tr(
                    f"{name} ({variation['num_rows']} rows, {variation['num_pegs']} pegs, {variation['num_colors']} colors)"
                )
            )
            for name, variation in app_config.variations.items()
        }

        self.variation_radio_buttons[
            app_config.settings.variation.current_value
        ].value = True

        blank_color_str = tr("Blank color")
        duplicate_colors_str = tr("Duplicate colors")

        labels = [rb.label for rb in self.variation_radio_buttons.values()] + [
            blank_color_str,
            duplicate_colors_str,
        ]

        yield Label(tr("Variation") + ":", classes="margin-bottom-1")
        self.variation_radio_set = RadioSet()
        with self.variation_radio_set:
            for rb in self.variation_radio_buttons.values():
                yield rb

        yield Label(tr("Additional options") + ":", classes="margin-bottom-1")
        self.blank_color_cb = Checkbox(
            blank_color_str,
            value=app_config.settings.blank_color.current_value,
            classes="margin-bottom-1",
        )
        self.duplicate_colors_cb = Checkbox(
            duplicate_colors_str,
            value=app_config.settings.duplicate_colors.current_value,
            classes="margin-bottom-1",
        )

        yield self.blank_color_cb
        yield self.duplicate_colors_cb

        self.variation_radio_set.styles.width = self.blank_color_cb.styles.width = (
            self.duplicate_colors_cb.styles.width
        ) = (
            len(max(labels, key=len))
            + BORDER_WIDTH
            + RADIO_SET_LEFT_PADDING_WIDTH
            + RADIO_SET_RIGHT_PADDING_WIDTH
            + BORDER_WIDTH
        )

        yield Footer()

    def on_mount(self) -> None:
        self.sub_title = tr("New game")

    def action_escape(self) -> None:
        self.dismiss(False)

    def action_next(self) -> None:
        app_config.settings.variation.old_value = (
            app_config.settings.variation.current_value
        )
        app_config.settings.variation.current_value = list(
            self.variation_radio_buttons.keys()
        )[self.variation_radio_set.pressed_index]

        app_config.settings.blank_color.old_value = (
            app_config.settings.blank_color.current_value
        )
        app_config.settings.blank_color.current_value = self.blank_color_cb.value

        app_config.settings.duplicate_colors.old_value = (
            app_config.settings.duplicate_colors.current_value
        )
        app_config.settings.duplicate_colors.current_value = (
            self.duplicate_colors_cb.value
        )

        self.dismiss(True)
