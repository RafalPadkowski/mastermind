from dataclasses import dataclass

from i18n import tr


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
            f"{self.name} ({self.num_rows} {tr('rows')}, "
            f"{tr(num_pegs_str)}, {self.num_colors} {tr('colors')})"
        )


variations: dict[str, Variation] = {
    "original": Variation(name="original", num_rows=10, num_pegs=4, num_colors=6),
    "mini": Variation(name="mini", num_rows=6, num_pegs=4, num_colors=6),
    "super": Variation(name="super", num_rows=12, num_pegs=5, num_colors=8),
}
