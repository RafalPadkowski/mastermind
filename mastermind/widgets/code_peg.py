from textual.widgets import Select

from mastermind.constants import BLANK_COLOR, CODE_PEG_COLORS
from mastermind.settings import app_settings


class CodePeg(Select):
    def __init__(self) -> None:
        num_colors: int = app_settings.variation.num_colors

        super().__init__(
            options=zip(CODE_PEG_COLORS, range(1, num_colors + 1)),
            prompt=BLANK_COLOR,
            classes="code_peg",
        )
