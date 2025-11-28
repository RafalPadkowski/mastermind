from textual.app import ComposeResult
from textual.screen import ModalScreen
from textual.widgets import Checkbox, Footer, Header, RadioButton, RadioSet
from tilsit_i18n import tr

from ..app_config import app_config
from ..bindings import NEW_GAME_BINDINGS


class NewGameScreen(ModalScreen[bool]):
    BINDINGS = NEW_GAME_BINDINGS

    def compose(self) -> ComposeResult:
        yield Header(icon=app_config.ui["new_game_icon"])

        with RadioSet():
            for name, variation in app_config.variations.items():
                yield RadioButton(
                    tr(
                        f"{name} ({variation['num_rows']} rows, {variation['num_pegs']} pegs, {variation['num_colors']} colors)"
                    )
                )
        # yield Checkbox(tr("Download data from the Internet"))
        yield Footer()

    def on_mount(self) -> None:
        self.sub_title = tr("New game")

    def action_escape(self) -> None:
        self.dismiss(False)

    def action_next(self) -> None:
        self.dismiss(True)
