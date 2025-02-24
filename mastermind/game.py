import random

from mastermind.settings import app_settings


class Game:
    def __init__(self) -> None:
        colors: list[int] = list(range(1, app_settings.variation.num_colors + 1))
        if app_settings.blank_color:
            colors.append(0)

        self.mastercode: list[int]
        if not app_settings.duplicate_colors:
            self.mastercode = random.sample(colors, k=app_settings.variation.num_pegs)
        else:
            self.mastercode = random.choices(colors, k=app_settings.variation.num_pegs)

    def check_code(self, breaker_code: list[int]):
        print(breaker_code)
