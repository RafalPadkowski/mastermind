from dataclasses import dataclass


@dataclass
class Settings:
    num_rows: int
    num_pegs: int
    num_colors: int
    blank_color: bool
    duplicate_colors: bool
