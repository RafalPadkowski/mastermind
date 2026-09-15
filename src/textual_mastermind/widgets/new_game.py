from textual.app import ComposeResult
from textual.screen import ModalScreen
from textual.widgets import Checkbox, Footer, Header, Label, RadioButton, RadioSet

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
                label=f"{name} ({variation['num_rows']} rows, {variation['num_pegs']} pegs, {variation['num_colors']} colors)"
            )
            for name, variation in app_config.variations.items()
        }

        self.variation_radio_buttons[
            app_config.settings["variation"]["current_value"]
        ].value = True

        blank_color_str = "Blank color"
        duplicate_colors_str = "Duplicate colors"

        labels = [rb.label for rb in self.variation_radio_buttons.values()] + [
            blank_color_str,
            duplicate_colors_str,
        ]

        yield Label("Variation:", classes="margin-bottom-1")
        self.variation_radio_set = RadioSet()
        with self.variation_radio_set:
            yield from self.variation_radio_buttons.values()

        yield Label(tr("Additional options") + ":", classes="margin-bottom-1")
        self.blank_symbol_cb = Checkbox(
            blank_symbol_str,
            value=app_config.settings.blank_symbol.current_value,
            classes="margin-bottom-1",
        )
        self.duplicate_symbols_cb = Checkbox(
            duplicate_symbols_str,
            value=app_config.settings.duplicate_symbols.current_value,
            classes="margin-bottom-1",
        )

        yield self.blank_symbol_cb
        yield self.duplicate_symbols_cb

        self.variation_radio_set.styles.width = self.blank_symbol_cb.styles.width = (
            self.duplicate_symbols_cb.styles.width
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

        app_config.settings.blank_symbol.old_value = (
            app_config.settings.blank_symbol.current_value
        )
        app_config.settings.blank_symbol.current_value = self.blank_symbol_cb.value

        app_config.settings.duplicate_symbols.old_value = (
            app_config.settings.duplicate_symbols.current_value
        )
        app_config.settings.duplicate_symbols.current_value = (
            self.duplicate_symbols_cb.value
        )

        self.dismiss(True)
