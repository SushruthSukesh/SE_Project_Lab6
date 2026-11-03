import pytest

from attendance_eligibility import (
    attendance_percent,
    attendance_warning,
    exam_eligibility,
)


@pytest.mark.parametrize(
    "attended,total_classes,medical_leave_days,expected",
    [
        (30, 40, 0, 75),
        (30, 40, 2, 80),
        (30, 40, 6, 87),
        (39, 40, 5, 100),
    ],
)
def test_attendance_percent_paths(
    attended, total_classes, medical_leave_days, expected
):
    assert attendance_percent(attended, total_classes, medical_leave_days) == expected


@pytest.mark.parametrize(
    "attended,total_classes",
    [(0, 0), (-1, 40), (41, 40)],
)
def test_attendance_percent_error_paths(attended, total_classes):
    with pytest.raises(ValueError):
        attendance_percent(attended, total_classes, 0)


@pytest.mark.parametrize(
    "percent,has_condonation,fees_paid,expected",
    [
        (80, False, False, "fees pending"),
        (75, False, True, "eligible"),
        (65, True, True, "eligible"),
        (65, False, True, "condonation required"),
        (64, True, True, "detained"),
    ],
)
def test_exam_eligibility_paths(
    percent, has_condonation, fees_paid, expected
):
    assert exam_eligibility(percent, has_condonation, fees_paid) == expected


@pytest.mark.parametrize(
    "percent,weeks_left,expected",
    [
        (85, 0, None),
        (75, 0, "reminder"),
        (74, 5, "critical"),
        (74, 4, "final notice"),
    ],
)
def test_attendance_warning_paths(percent, weeks_left, expected):
    assert attendance_warning(percent, weeks_left) == expected
