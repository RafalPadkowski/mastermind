from textual.widgets import Label

from .. import app_config


class Check(Label):
    def __init__(self) -> None:
        variation = app_config.variations[app_config.settings.variation.current_value]

        self.default_text = (
            f"{app_config.ui['check_default_text']} " * variation["num_pegs"]
        )[:-1]
        self.hover_text = (
            f"{app_config.ui['check_hover_text']} " * variation["num_pegs"]
        )[:-1]

        super().__init__(self.default_text, id="check", classes="check")

    def on_enter(self) -> None:
        self.update(self.hover_text)

    def on_leave(self) -> None:
        self.update(self.default_text)
