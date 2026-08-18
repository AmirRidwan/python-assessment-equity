from decimal import Decimal
from typing import Optional, Literal

SignalType = Literal["golden_cross", "death_cross"]


def detect_crossover(
    previous_short_ma: Optional[Decimal],
    previous_long_ma: Optional[Decimal],
    current_short_ma: Optional[Decimal],
    current_long_ma: Optional[Decimal],
) -> Optional[SignalType]:

    # Detect a crossover between the previous and current MA states.
    # Golden cross:
    #     previous short <= previous long
    #     current short > current long
    # Death cross:
    #     previous short >= previous long
    #     current short < current long

    if (
        previous_short_ma is None
        or previous_long_ma is None
        or current_short_ma is None
        or current_long_ma is None
    ):
        return None

    if previous_short_ma <= previous_long_ma and current_short_ma > current_long_ma:
        return "golden_cross"

    if previous_short_ma >= previous_long_ma and current_short_ma < current_long_ma:
        return "death_cross"

    return None
