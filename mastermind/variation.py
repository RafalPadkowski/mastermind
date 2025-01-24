from dataclasses import dataclass

from mastermind.i18n import _


@dataclass(frozen=True)
class Variation:
    name: str
    num_rows: int
    num_pegs: int
    num_colors: int

    @property
    def description(self) -> str:
        num_pegs_str = f"{self.num_pegs} pegs"

        return (
            f"{self.name} ({self.num_rows} {_('rows')}, "
            f"{_(num_pegs_str)}, {self.num_colors} {_('colors')})"
        )
