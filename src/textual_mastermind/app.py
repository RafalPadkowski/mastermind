from typing import cast

from rich.text import Text
from textual import on, work
from textual.app import App, ComposeResult
from textual.containers import Horizontal
from textual.widgets import Button, Footer, Header, Label

from .app_config import app_config
from .bindings import GlOBAL_BINDINGS
from .commands import AboutCommand
from .game import Game
from .widgets.board import Board
from .widgets.new_game import NewGameScreen
from .widgets.panel import Panel


class MastermindApp(App[None]):
    CSS_PATH = "styles.tcss"
    COMMANDS = App.COMMANDS | {AboutCommand}
    BINDINGS = GlOBAL_BINDINGS

    def __init__(self) -> None:
        super().__init__()

        self.body: Horizontal
        self.panel: Panel
        self.board: Board

        self.game: Game

    def compose(self) -> ComposeResult:
        yield Header(icon=app_config.ui["main_icon"])

        self.body = Horizontal()
        yield self.body

        yield Footer()

    def on_mount(self) -> None:
        self.title = app_config.ui["title"]
        self.create_new_game()

    def create_new_game(self) -> None:
        if hasattr(self, "game"):
            self.panel.remove()
            self.board.remove()

        blank_str = f"blank: {'on' if app_config.allow_blank_color else 'off'}"
        duplicates_str = (
            f"duplicates: {'on' if app_config.allow_duplicate_colors else 'off'}"
        )

        self.sub_title = (
            f"{app_config.variation_name.capitalize()} - {blank_str} - {duplicates_str}"
        )

        self.panel = Panel()
        self.body.mount(self.panel)

        self.board = Board()
        self.body.mount(self.board)

        self.set_focus(self.panel)

        self.game = Game()

    @on(Button.Pressed, ".code_peg")
    def on_code_peg_pressed(self, event: Button.Pressed):
        idx = cast(int, self.panel.select.value)
        style = app_config.ui["code_style"]

        if idx == 0:
            event.button.label = Text(
                app_config.ui["code_blank_letter"], style=f"{style}"
            )
        else:
            idx -= 1
            letter = app_config.ui["code_letters"][idx]
            color = app_config.ui["code_colors"][idx]
            event.button.label = Text(letter, style=f"{color} {style}")

    @on(Button.Pressed, ".check")
    def on_check_click(self) -> None:
        breaker_code: list[int] = []
        for code_peg in self.board.current_row.code_pegs:
            code_letter = cast(str, code_peg.label)

            color: int
            if code_letter == app_config.ui["code_blank_letter"]:
                color = 0
            else:
                color = app_config.ui["code_letters"].index(code_letter) + 1

            breaker_code.append(color)

        num_red_pegs: int
        num_white_pegs: int
        num_red_pegs, num_white_pegs = self.game.check_code(breaker_code)

        self.board.current_row.query_one("#check").remove()

        feedback_red_letter = app_config.ui["feedback_letters"][0]
        feedback_red_color = app_config.ui["feedback_colors"][0]
        feedback_white_letter = app_config.ui["feedback_letters"][1]
        feedback_white_color = app_config.ui["feedback_colors"][1]
        feedback_blank_letter = app_config.ui["feedback_blank_letter"]
        feedback_style = app_config.ui["feedback_style"]

        self.board.current_row.mount(
            Label(
                Text("").join(
                    [
                        Text(
                            (feedback_red_letter + " ") * num_red_pegs,
                            style=f"{feedback_red_color} {feedback_style}",
                        ),
                        Text(
                            (feedback_white_letter + " ") * num_white_pegs,
                            style=f"{feedback_white_color} {feedback_style}",
                        ),
                        Text(
                            (feedback_blank_letter + " ")
                            * (self.game.num_pegs - num_red_pegs - num_white_pegs),
                            style=f"{feedback_style}",
                        ),
                    ]
                ),
                classes="feedback_pegs",
            )
        )

        self.board.current_row.disabled = True

        if num_red_pegs == self.game.num_pegs:
            self.notify("Congratulations!")
        else:
            if self.board.current_row_number < self.game.num_rows:
                self.board.add_row()
            else:
                maker_code: list[int] = self.game.get_maker_code()
                maker_code_str: str = ""
                for color in maker_code:
                    if color == 0:
                        maker_code_str += app_config.ui["code_blank_letter"] + " "
                    else:
                        maker_code_str += app_config.ui["code_letters"][color - 1] + " "

                self.notify(
                    f"Better luck next time\nCode: {maker_code_str}",
                    timeout=60,
                )

    @work
    async def action_new_game(self) -> None:
        new_game_screen = NewGameScreen()

        if await self.push_screen_wait(new_game_screen):
            self.create_new_game()
