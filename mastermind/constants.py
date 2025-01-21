from pathlib import Path
from typing import Final

from mastermind.variation import Variation

ICON: Final[str] = "❔"

SETTINGS_PATH: Final[Path] = Path(__file__).parent / "settings.toml"

BLANK_COLOR: Final[str] = "⭕"
CODE_PEG_COLORS: Final[list[str]] = ["🔴", "🟡", "🟣", "🟢", "🟤", "🔵", "⚪", "🟠"]
FEEDBACK_PEG_COLORS: Final[list[str]] = ["🔴", "⚪"]

VARIATIONS: Final[dict[str, Variation]] = {
    "original": Variation(num_rows=10, num_pegs=4, num_colors=6),
    "mini": Variation(num_rows=6, num_pegs=4, num_colors=6),
    "super": Variation(num_rows=12, num_pegs=5, num_colors=8),
}
