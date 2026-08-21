from decimal import Decimal

from app.business_logic.moving_average import calculate_moving_average


def test_moving_average():
    prices = [
        Decimal("10"),
        Decimal("20"),
        Decimal("30"),
        Decimal("40"),
        Decimal("50"),
    ]

    result = calculate_moving_average(prices, 3)

    assert result == [
        None,
        None,
        Decimal("20"),
        Decimal("30"),
        Decimal("40"),
    ]


def test_moving_average_accepts_float_values():
    prices = [10.0, 20.0, 30.0]

    result = calculate_moving_average(prices, 2)

    assert result == [
        None,
        Decimal("15"),
        Decimal("25"),
    ]
