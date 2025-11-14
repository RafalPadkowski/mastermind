import random

from .app_config import Variation


class Game:
    def __init__(
        self, variation: Variation, blank_color: bool, duplicate_colors: bool
    ) -> None:
        self.num_rows = variation["num_rows"]
        self.num_pegs = variation["num_pegs"]
        self.num_colors = variation["num_colors"]

        colors: list[int] = list(range(1, self.num_colors + 1))
        if blank_color:
            colors.append(0)

        self.maker_code: list[int]
        if duplicate_colors:
            self.maker_code = random.choices(colors, k=self.num_pegs)
        else:
            self.maker_code = random.sample(colors, k=self.num_pegs)

    def check_code(self, breaker_code: list[int]) -> tuple[int, int]:
        breaker_code_no_reds = [
            color
            for i, color in enumerate(breaker_code)
            if self.maker_code[i] != breaker_code[i]
        ]
        maker_code_no_reds = [
            color
            for i, color in enumerate(self.maker_code)
            if self.maker_code[i] != breaker_code[i]
        ]

        num_red_pegs: int = len(breaker_code) - len(breaker_code_no_reds)

        num_white_pegs: int = 0
        for color in breaker_code_no_reds:
            if color in maker_code_no_reds:
                num_white_pegs += 1
                maker_code_no_reds.remove(color)

        return num_red_pegs, num_white_pegs

    def get_maker_code(self) -> list[int]:
        return self.maker_code
