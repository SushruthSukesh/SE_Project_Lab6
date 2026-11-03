import pytest

from attendance_eligibility import (
    attendance_percent,
    attendance_warning,
    exam_eligibility,
)


def test_attendance_percent_with_medical_leave():
    assert attendance_percent(30, 40, 2) == 80


def test_attendance_percent_caps_medical_leave():
    assert attendance_percent(30, 40, 10) == 87


def test_attendance_percent_caps_credited_classes():
    assert attendance_percent(39, 40, 5) == 100


@pytest.mark.parametrize(
    "attended,total_classes,medical_leave_days",
    [(0, 0, 0), (-1, 40, 0), (41, 40, 0)],
)
def test_attendance_percent_rejects_invalid_counts(
    attended, total_classes, medical_leave_days
):
    with pytest.raises(ValueError):
        attendance_percent(attended, total_classes, medical_leave_days)


def test_exam_eligibility_when_fees_are_pending():
    assert exam_eligibility(90, True, False) == "fees pending"


def test_exam_eligibility_for_high_attendance():
    assert exam_eligibility(75, False, True) == "eligible"


def test_exam_eligibility_requires_condonation():
    assert exam_eligibility(65, False, True) == "condonation required"


def test_exam_eligibility_with_condonation():
    assert exam_eligibility(65, True, True) == "eligible"


def test_exam_eligibility_detains_low_attendance():
    assert exam_eligibility(64, False, True) == "detained"


def test_attendance_warning_for_high_attendance():
    assert attendance_warning(85, 1) is None


def test_attendance_warning_for_mid_range_attendance():
    assert attendance_warning(75, 1) == "reminder"


def test_attendance_warning_for_critical_low_attendance():
    assert attendance_warning(74, 5) == "critical"


def test_attendance_warning_for_final_notice():
    assert attendance_warning(74, 4) == "final notice"
