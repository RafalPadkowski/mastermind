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

        self.variation_radio_buttons[app_config.variation_name].value = True

        blank_color_str = "Allow blank color"
        duplicate_colors_str = "Allow duplicate colors"

        yield Label("Variation:", classes="margin-bottom-1")
        self.variation_radio_set = RadioSet()
        with self.variation_radio_set:
            yield from self.variation_radio_buttons.values()

        yield Label("Additional options:", classes="margin-bottom-1")
        self.blank_color_cb = Checkbox(
            blank_color_str,
            value=app_config.allow_blank_color,
            classes="margin-bottom-1",
        )
        self.duplicate_colors_cb = Checkbox(
            duplicate_colors_str,
            value=app_config.allow_duplicate_colors,
            classes="margin-bottom-1",
        )

        yield self.blank_color_cb
        yield self.duplicate_colors_cb

        labels = [rb.label for rb in self.variation_radio_buttons.values()] + [
            blank_color_str,
            duplicate_colors_str,
        ]

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
        self.sub_title = "New game"

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


def save_settings(config_file: str, settings: Dataclass):
    with open(config_file, mode="rt", encoding="utf-8") as f:
        config_doc = tomlkit.load(f)

    config_dict = cast(dict[str, Any], config_doc)

    for field in fields(settings):
        setting: SettingType = getattr(settings, field.name)
        config_dict["settings"][field.name]["current_value"] = setting.current_value

    with open(config_file, mode="wt", encoding="utf-8") as f:
        tomlkit.dump(config_doc, f)  # type: ignore[arg-type]
