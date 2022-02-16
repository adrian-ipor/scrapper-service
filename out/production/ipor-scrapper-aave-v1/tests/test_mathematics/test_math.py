from assertpy import assert_that
from expects import expect, raise_error

from mathematics import maths


def test_to_percent_for_value_above_zero():
    # Given
    value = 0.1
    # # When
    result = maths.to_percent(value)
    # # Then
    assert_that(result).is_equal_to(10)


def test_to_percent_for_value_below_zero():
    # Given
    value = -0.5
    # When
    result = maths.to_percent(value)
    # Then
    assert_that(result).is_equal_to(-50)


def test_to_percent_for_value_is_string():
    # Given
    value = "string"
    # When and then
    expect(lambda: maths.to_percent(value)).to(raise_error(ValueError))


def test_to_percent_for_value_equal_to_zero():
    # Given
    value = 0
    # When
    result = maths.to_percent(value)
    # Then
    assert_that(result).is_equal_to(0)


def test_to_percent_for_value_equal_to_none():
    # Given
    value = None
    # When and then
    expect(lambda: maths.to_percent(value)).to(raise_error(ValueError))


def test_to_decimal_for_except_value():
    # Given
    value = 2
    decimal = 10
    # When
    result = maths.to_decimal(decimal, value)
    # Then
    assert_that(result).is_equal_to(0.0000000002)


def test_to_decimal_for_value_equal_to_string():
    # Given
    value = "string"
    decimal = 10
    # When and then
    expect(lambda: maths.to_decimal(decimal, value)).to(raise_error(ValueError))


def test_to_decimal_for_value_equal_to_none():
    # Given
    value = None
    decimal = 10
    # When and then
    expect(lambda: maths.to_decimal(decimal, value)).to(raise_error(ValueError))


def test_to_decimal_for_decimal_equal_to_none():
    # Given
    value = 1234
    decimal = None
    # When and then
    expect(lambda: maths.to_decimal(decimal, value)).to(raise_error(ValueError))
