from decimal import Decimal
from typing import Iterable


def validate_total_weight(
    existing_weights: Iterable[Decimal],
    new_weight: Decimal,
) -> bool:
    
    # Return True when adding new_weight keeps the manager's
    # total portfolio weight at or below 100%.
    
    total = sum(existing_weights, Decimal("0"))
    return total + new_weight <= Decimal("100")


def validate_updated_weight(
    existing_weights: Iterable[Decimal],
    old_weight: Decimal,
    new_weight: Decimal,
) -> bool:
    
    # Validate an updated holding by removing the old weight
    # before adding the new weight.
    
    total_without_old = sum(existing_weights, Decimal("0")) - old_weight

    return total_without_old + new_weight <= Decimal("100")
