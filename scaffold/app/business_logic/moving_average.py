from decimal import Decimal
from typing import Sequence


def calculate_moving_average(
    prices: Sequence[Decimal],
    window: int,
) -> list[Decimal | None]:

    # Calculate a rolling moving average.
    # Values before enough observations exist are returned as None.

    if window <= 0:
        raise ValueError("window must be greater than zero")

    # Normalize all inputs to Decimal.
    decimal_prices = [
        value if isinstance(value, Decimal) else Decimal(str(value)) for value in prices
    ]

    results: list[Decimal | None] = []

    for index in range(len(decimal_prices)):
        if index + 1 < window:
            results.append(None)
            continue

        window_prices = decimal_prices[index - window + 1 : index + 1]

        average = sum(window_prices, Decimal("0")) / Decimal(window)

        results.append(average)

    return results
