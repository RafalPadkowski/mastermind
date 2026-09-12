from pprint import pprint

import textual_mastermind.app_config
from textual_mastermind.app import MastermindApp


def main():
    pprint(textual_mastermind.app_config.app_config)
    # return
    app = MastermindApp()
    app.run()
