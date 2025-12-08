from textual.app import ComposeResult
from textual.containers import VerticalScroll
from textual.message import Message
from textual.widgets import Button

from ..app_config import app_config


class SymbolButton(Button):
    class Toggled(Message):
        def __init__(self, sender: "SymbolButton") -> None:
            super().__init__()
            self.sender = sender

    def on_click(self):
        self.post_message(self.Toggled(sender=self))


class Panel(VerticalScroll):
    def __init__(self) -> None:
        super().__init__()
        self.active_color = 0

    def compose(self) -> ComposeResult:
        variation = app_config.variation

        self.symbol_buttons: list[SymbolButton] = [
            SymbolButton(app_config.ui["code_blank_symbol"], classes="active")
        ]

        self.symbol_buttons.extend(
            [
                SymbolButton(symbol)
                for symbol in app_config.ui["code_symbols"][: variation["num_symbols"]]
            ]
        )

        for symbol_button in self.symbol_buttons:
            yield symbol_button

    def on_symbol_button_toggled(self, message: SymbolButton.Toggled):
        for symbol_button in self.symbol_buttons:
            symbol_button.remove_class("active")

        message.sender.add_class("active")

        self.active_symbol = self.symbol_buttons.index(message.sender)
