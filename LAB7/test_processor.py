from hypothesis import given, strategies as st

from attendance_eligibility_parser import (
    attendance_from_ratio,
    attendance_from_register,
    normalize_srn,
)


@given(st.one_of(st.text(), st.none(), st.integers()))
def test_normalize_srn_no_crash(value):
    try:
        result = normalize_srn(value)
    except Exception as error:
        raise AssertionError(f"normalize_srn crashed for {value!r}: {error}") from error
    assert isinstance(result, str)


@given(st.one_of(st.text(), st.none(), st.integers()))
def test_attendance_from_ratio_no_crash(value):
    try:
        result = attendance_from_ratio(value)
    except Exception as error:
        raise AssertionError(
            f"attendance_from_ratio crashed for {value!r}: {error}"
        ) from error
    assert isinstance(result, int)
    assert 0 <= result <= 100


@given(st.one_of(st.text(), st.none(), st.integers()))
def test_attendance_from_register_no_crash(value):
    try:
        result = attendance_from_register(value)
    except Exception as error:
        raise AssertionError(
            f"attendance_from_register crashed for {value!r}: {error}"
        ) from error
    assert isinstance(result, int)
    assert 0 <= result <= 100


def test_valid_values_are_processed():
    assert normalize_srn(" pes1 ug23 cs001 ") == "PES1UG23CS001"
    assert attendance_from_ratio("30/40") == 75
    assert attendance_from_register("PPAPP") == 80
