from dataclasses import dataclass


@dataclass(frozen=True)
class Variation:
    name: str
    num_rows: int
    num_pegs: int
    num_colors: int

    @property
    def description(self) -> str:
        return (
            f"{self.name} ({self.num_rows} rows, "
            f"{self.num_pegs} pegs, {self.num_colors} colors)"
        )
