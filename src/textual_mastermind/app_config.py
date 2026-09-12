from importlib.resources import files

import tomlkit

with files(__package__).joinpath("config.toml").open("r", encoding="utf-8") as config:
    app_config = tomlkit.load(config)
