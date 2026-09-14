from typing import cast

from textual import on, work
from textual.app import App, ComposeResult
from textual.containers import Horizontal
from textual.events import Click
from textual.widgets import Button, Footer, Header, Label

from .app_config import app_config
from .bindings import NEW_GAME_BINDINGS, GlOBAL_BINDINGS
from .game import Game
from .widgets.board import Board
from .widgets.panel import Panel

# from .widgets.new_game import NewGameScreen

__title__ = "Mastermind"


class MastermindApp(App[None]):
    CSS_PATH = "styles.tcss"
    BINDINGS = GlOBAL_BINDINGS

    def __init__(self) -> None:
        super().__init__()

        self.panel: Panel
        self.board: Board

        self.game: Game

    def compose(self) -> ComposeResult:
        yield Header(icon=app_config.ui["main_icon"])
        yield Horizontal(id="body")
        yield Footer()

    def on_mount(self) -> None:
        self.title = __title__
        self.create_new_game()

    def create_new_game(self) -> None:
        if hasattr(self, "game"):
            # self.panel.remove()
            self.board.remove()

        self.panel = Panel()
        self.board = Board()
        body: Horizontal = self.query_one("#body", Horizontal)
        body.mount(self.panel)
        body.mount(self.board)

        self.set_focus(self.panel)

        # self.game = Game()

    @on(Button.Pressed, ".code_peg")
    def on_code_peg_pressed(self, event: Button.Pressed):
        active_symbol: int = self.panel.active_symbol
        if active_symbol != 0:
            event.button.label = app_config.ui["code_symbols"][active_symbol - 1]
        else:
            event.button.label = app_config.ui["code_blank_symbol"]

    @on(Click, ".check")
    def on_check_click(self) -> None:
        breaker_code: list[int] = []
        for code_peg in self.board.current_row.code_pegs:
            symbol_str = cast(str, code_peg.label)

            symbol: int
            if symbol_str == app_config.ui["code_blank_symbol"]:
                symbol = 0
            else:
                symbol = app_config.ui["code_symbols"].index(symbol_str) + 1

            breaker_code.append(symbol)

        num_red_pegs: int
        num_white_pegs: int
        num_red_pegs, num_white_pegs = self.game.check_code(breaker_code)

        self.board.current_row.query_one("#check").remove()

        self.board.current_row.mount(
            Label(
                "".join(
                    [
                        (app_config.ui["feedback_symbols"][0] + " ") * num_red_pegs,
                        (app_config.ui["feedback_symbols"][1] + " ") * num_white_pegs,
                        (app_config.ui["feedback_blank_symbol"] + " ")
                        * (self.game.num_pegs - num_red_pegs - num_white_pegs),
                    ]
                ),
                classes="feedback_pegs",
            )
        )

        self.board.current_row.disabled = True

        if num_red_pegs == self.game.num_pegs:
            self.notify(tr("Congratulations!"))
        else:
            if self.board.current_row_number < self.game.num_rows:
                self.board.add_row()
            else:
                maker_code: list[int] = self.game.get_maker_code()
                maker_code_str: str = ""
                for symbol in maker_code:
                    if symbol == 0:
                        maker_code_str += app_config.ui["code_blank_symbol"] + " "
                    else:
                        maker_code_str += (
                            app_config.ui["code_symbols"][symbol - 1] + " "
                        )

                self.notify(
                    f"{tr('Better luck next time')}\n{tr('Code')}: {maker_code_str}",
                    timeout=60,
                )

    @work
    async def action_new_game(self) -> None:
        new_game_screen = NewGameScreen()
        translate_bindings(screen=new_game_screen, bindings=NEW_GAME_BINDINGS)

        if await self.push_screen_wait(new_game_screen):
            self.create_new_game()

            if any(
                [
                    app_config.settings.variation.changed,
                    app_config.settings.duplicate_symbols.changed,
                    app_config.settings.blank_symbol.changed,
                ]
            ):
                save_settings(str(CONFIG_FILE), app_config.settings)
