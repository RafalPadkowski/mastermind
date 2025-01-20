from dataclasses import dataclass


@dataclass(frozen=True)
class Variation:
    num_rows: int
    num_pegs: int
    num_colors: int
