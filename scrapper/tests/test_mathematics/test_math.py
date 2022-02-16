from assertpy import assert_that
from expects import expect, raise_error

import sys, os
myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../')

from mathematics import maths


def to_percent_for_value_above_zero_except_success():
    # Given
    value = 0.1
    # # When
    result = maths.to_percent(value)
    # # Then
    assert_that(result).is_equal_to(10)


def to_percent_for_value_below_zero_except_success():
    # Given
    value = -0.5
    # When
    result = maths.to_percent(value)
    # Then
    assert_that(result).is_equal_to(-50)


def to_percent_for_value_is_string_except_error():
    # Given
    value = "string"
    # When and then
    expect(lambda: maths.to_percent(value)).to(raise_error(ValueError))


def to_percent_for_value_equal_to_zero_except_success():
    # Given
    value = 0
    # When
    result = maths.to_percent(value)
    # Then
    assert_that(result).is_equal_to(0)


def to_percent_for_value_equal_to_none_except_error():
    # Given
    value = None
    # When and then
    expect(lambda: maths.to_percent(value)).to(raise_error(ValueError))


def to_decimal_for_except_value_except_success():
    # Given
    value = 2
    decimal = 10
    # When
    result = maths.to_decimal(decimal, value)
    # Then
    assert_that(result).is_equal_to(0.0000000002)


def to_decimal_for_value_equal_to_string_except_error():
    # Given
    value = "string"
    decimal = 10
    # When and then
    expect(lambda: maths.to_decimal(decimal, value)).to(raise_error(ValueError))


def to_decimal_for_value_equal_to_none_except_error():
    # Given
    value = None
    decimal = 10
    # When and then
    expect(lambda: maths.to_decimal(decimal, value)).to(raise_error(ValueError))


def test_to_decimal_for_decimal_equal_to_none_except_error():
    # Given
    value = 1234
    decimal = None
    # When and then
    expect(lambda: maths.to_decimal(decimal, value)).to(raise_error(ValueError))
