from pprint import pprint

from textual_mastermind import app_config
from textual_mastermind.app import MastermindApp


def main():
    pprint(app_config.config_dict)
    app = MastermindApp()
    app.run()
