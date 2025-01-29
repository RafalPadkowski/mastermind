from textual.events import Click
from textual.widgets._header import HeaderIcon
from textual_utils import AppMetadata

from mastermind.screens import AboutScreen


class MastermindHeaderIcon(HeaderIcon):
    def __init__(self, app_metadata: AppMetadata) -> None:
        super().__init__()

        self.app_metadata = app_metadata

    async def on_click(self, event: Click) -> None:
        self.app.push_screen(AboutScreen(self.app_metadata))
