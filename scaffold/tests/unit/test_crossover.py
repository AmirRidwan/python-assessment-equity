from decimal import Decimal

from app.business_logic.crossover import detect_crossover


def test_golden_cross():
    result = detect_crossover(
        Decimal("100"),
        Decimal("105"),
        Decimal("110"),
        Decimal("105"),
    )

    assert result == "golden_cross"


def test_death_cross():
    result = detect_crossover(
        Decimal("110"),
        Decimal("105"),
        Decimal("100"),
        Decimal("105"),
    )

    assert result == "death_cross"


def test_no_crossover():
    result = detect_crossover(
        Decimal("110"),
        Decimal("105"),
        Decimal("115"),
        Decimal("105"),
    )

    assert result is None


def test_no_crossover_when_ma_is_missing():
    result = detect_crossover(
        None,
        None,
        Decimal("100"),
        Decimal("105"),
    )

    assert result is None
