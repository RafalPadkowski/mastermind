from textual.widgets import Select

from mastermind.constants import BLANK_COLOR, CODE_PEG_COLORS
from mastermind.settings import Settings, get_settings


class CodePeg(Select):
    def __init__(self) -> None:
        app_settings: Settings = get_settings()
        num_colors: int = app_settings.variation.num_colors

        super().__init__(
            options=zip(CODE_PEG_COLORS, range(1, num_colors + 1)),
            prompt=BLANK_COLOR,
            classes="code_peg",
        )
