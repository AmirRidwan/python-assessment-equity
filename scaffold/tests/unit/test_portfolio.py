from decimal import Decimal

from app.business_logic.portfolio import (
    validate_total_weight,
    validate_updated_weight,
)


def test_total_weight_under_100():
    assert validate_total_weight(
        [
            Decimal("20"),
            Decimal("30"),
        ],
        Decimal("40"),
    )


def test_total_weight_exactly_100():
    assert validate_total_weight(
        [
            Decimal("20"),
            Decimal("30"),
        ],
        Decimal("50"),
    )


def test_total_weight_over_100():
    assert not validate_total_weight(
        [
            Decimal("20"),
            Decimal("30"),
        ],
        Decimal("51"),
    )


def test_update_weight_exactly_100():
    assert validate_updated_weight(
        [
            Decimal("30"),
            Decimal("30"),
            Decimal("20"),
        ],
        Decimal("30"),
        Decimal("50"),
    )


def test_update_weight_over_100():
    assert not validate_updated_weight(
        [
            Decimal("30"),
            Decimal("30"),
            Decimal("20"),
        ],
        Decimal("30"),
        Decimal("51"),
    )
