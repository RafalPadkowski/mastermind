from typing import TYPE_CHECKING

from mastermind.settings import app_settings
from mastermind.widgets.board import Board

if TYPE_CHECKING:
    from mastermind.app import MastermindApp


def new(self: "MastermindApp", game_exists: bool = True):
    if game_exists:
        self.board.remove()

    self.board = Board()
    self.mount(self.board)


def check_code(self: "MastermindApp"):
    self.board.current_row.children[-1].remove()
    self.board.current_row.disabled = True

    for code_peg in self.board.current_row.code_pegs:
        code_peg.children[0].children[1].remove()

    if self.board.current_row_number < app_settings.variation.num_rows:
        self.board.add_row()
    else:
        self.notify("Koniec", timeout=2)
