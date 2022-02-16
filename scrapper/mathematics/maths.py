import logger

ray_unit = 27


def to_percent(input_value):
    if isinstance(input_value, float) or isinstance(input_value, int):
        return input_value * 100
    else:
        raise ValueError("Value is not a integer or float")


def to_decimal(decimal_number, input_value):
    if isinstance(input_value, int) and isinstance(decimal_number, int):
        return input_value * 10 ** -decimal_number
    else:
        raise ValueError("Value is not a integer or float")
