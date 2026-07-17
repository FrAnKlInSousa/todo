from decimal import ROUND_HALF_UP, Decimal


def arredonda_casas_decimais(valor: float):
    return float(
        Decimal(str(valor)).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    )
