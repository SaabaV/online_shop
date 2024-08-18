from decimal import Decimal


def round_price_to_99_cents(price):
    rounded_price = (price // Decimal(1)) + Decimal('0.99')
    return rounded_price
