from typing import cast

from textual.app import ComposeResult
from textual.screen import ModalScreen
from textual.widgets import Checkbox, Footer, Header, Label, RadioButton, RadioSet

from ..app_config import Variation, app_config
from ..bindings import NEW_GAME_BINDINGS

BORDER_WIDTH = 1
RADIO_SET_LEFT_PADDING_WIDTH = 5
RADIO_SET_RIGHT_PADDING_WIDTH = 2


class NewGameScreen(ModalScreen[bool]):
    BINDINGS = NEW_GAME_BINDINGS

    def compose(self) -> ComposeResult:
        yield Header(icon=app_config.ui["new_game_icon"])

        variations = cast(dict[str, Variation], app_config.variations)

        self.variation_radio_buttons = {
            name: RadioButton(
                label=f"{name} ({variation['num_rows']} rows, {variation['num_pegs']} pegs, {variation['num_colors']} colors)"
            )
            for name, variation in variations.items()
        }

        self.variation_radio_buttons[app_config.variation_name].value = True

        allow_blank_color_str = "Allow blank color"
        allow_duplicate_colors_str = "Allow duplicate colors"

        yield Label("Variation:", classes="margin-bottom-1")
        self.variation_radio_set = RadioSet()
        with self.variation_radio_set:
            yield from self.variation_radio_buttons.values()

        yield Label("Additional options:", classes="margin-bottom-1")
        self.allow_blank_color_cb = Checkbox(
            allow_blank_color_str,
            value=app_config.allow_blank_color,
            classes="margin-bottom-1",
        )
        self.allow_duplicate_colors_cb = Checkbox(
            allow_duplicate_colors_str,
            value=app_config.allow_duplicate_colors,
            classes="margin-bottom-1",
        )

        yield self.allow_blank_color_cb
        yield self.allow_duplicate_colors_cb

        labels = [rb.label for rb in self.variation_radio_buttons.values()] + [
            allow_blank_color_str,
            allow_duplicate_colors_str,
        ]

        self.variation_radio_set.styles.width = (
            self.allow_blank_color_cb.styles.width
        ) = self.allow_duplicate_colors_cb.styles.width = (
            len(max(labels, key=len))
            + BORDER_WIDTH
            + RADIO_SET_LEFT_PADDING_WIDTH
            + RADIO_SET_RIGHT_PADDING_WIDTH
            + BORDER_WIDTH
        )

        yield Footer()

    def on_mount(self) -> None:
        self.sub_title = "New game"

    def action_escape(self) -> None:
        self.dismiss(False)

    def action_next(self) -> None:
        changed_settings: list[str] = []

        variation_name: str = list(self.variation_radio_buttons.keys())[
            self.variation_radio_set.pressed_index
        ]

        if variation_name != app_config.variation_name:
            app_config.variation_name = variation_name
            changed_settings.append("variation_name")

        allow_blank_color = self.allow_blank_color_cb.value

        if allow_blank_color != app_config.allow_blank_color:
            app_config.allow_blank_color = allow_blank_color
            changed_settings.append("allow_blank_color")

        allow_duplicate_colors = self.allow_duplicate_colors_cb.value

        if allow_duplicate_colors != app_config.allow_duplicate_colors:
            app_config.allow_duplicate_colors = allow_duplicate_colors
            changed_settings.append("allow_duplicate_colors")

        app_config.save_settings(*changed_settings)

        self.dismiss(True)
