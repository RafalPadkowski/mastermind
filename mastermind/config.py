from dataclasses import dataclass


@dataclass
class General:
    icon: str


@dataclass
class Colors:
    code_peg_colors: list[str]
    feedback_peg_colors: list[str]
    blank_color: str


@dataclass
class Variation:
    num_rows: int
    num_pegs: int
    num_colors: int


@dataclass
class Config:
    general: General
    colors: Colors
    variations: dict[str, Variation]


app_config = Config(
    general=General(icon="❔"),
    colors=Colors(
        code_peg_colors=["🔴", "🟡", "🟣", "🟢", "🟤", "🔵", "⚪", "🟠"],
        feedback_peg_colors=["🔴", "⚪"],
        blank_color="⭕",
    ),
    variations={
        "original": Variation(num_rows=10, num_pegs=4, num_colors=6),
        "mini": Variation(num_rows=6, num_pegs=4, num_colors=6),
        "super": Variation(num_rows=12, num_pegs=5, num_colors=8),
    },
)
