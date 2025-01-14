from textual.app import App, ComposeResult
from textual.containers import Horizontal
from textual.widgets import Button, Footer, Header, Select, Static


class ColorPeg(Select):
    def __init__(self):
        options = [
            (":red_circle:", 1),
            (":yellow_circle:", 2),
            (":purple_circle:", 3),
            (":green_circle:", 4),
            (":brown_circle:", 5),
            (":blue_circle:", 6),
        ]

        super().__init__(options=options, prompt="⭕", classes="color_peg")


class MastermindApp(App):
    TITLE = "Mastermind"

    CSS_PATH = "mm.tcss"

    def compose(self) -> ComposeResult:
        yield Header(icon="❔")

        yield Horizontal(
            Static("01", classes="num"),
            Static("🔵", classes="static_color_peg"),
            Static("🔴", classes="static_color_peg"),
            Static("🟢", classes="static_color_peg"),
            Static("🟣", classes="static_color_peg"),
            Static("🔴 ⚪ ⭕ ⭕", classes="feedback"),
            classes="row",
        )

        yield Horizontal(
            Static("02", classes="num"),
            ColorPeg(),
            ColorPeg(),
            ColorPeg(),
            ColorPeg(),
            Button("❔", classes="check"),
            classes="row",
        )

        yield Footer()
