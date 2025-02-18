from textual.widgets import Select

from mastermind.constants import BLANK_COLOR, CODE_PEG_COLORS


class CodePeg(Select):
    def __init__(self) -> None:
        # num_colors: int = current_app.settings.variation.num_colors
        num_colors = 6

        super().__init__(
            options=zip(CODE_PEG_COLORS, range(1, num_colors + 1)),
            prompt=BLANK_COLOR,
            classes="code_peg",
        )
