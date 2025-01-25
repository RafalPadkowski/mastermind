from textual.events import Click
from textual.widgets._header import HeaderIcon

from mastermind.screens import AboutScreen


class MastermindHeaderIcon(HeaderIcon):
    async def on_click(self, event: Click) -> None:
        self.app.push_screen(AboutScreen())
