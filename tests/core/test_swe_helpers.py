from datetime import datetime, timezone
from unittest.mock import patch

from at.core.sweHelpers import floatToHMS, jdtToDateTime


def test_float_to_hms_handles_fractional_seconds_without_overflow():
	h, m, s = floatToHMS(1 + (2 / 60) + (59.999999 / 3600))
	assert (h, m, s) == (1, 3, 0)


def test_float_to_hms_preserves_basic_hms_conversion():
	h, m, s = floatToHMS(6.5)
	assert (h, m, s) == (6, 30, 0)


def test_float_to_hms_carries_to_next_hour_when_seconds_round_up():
	h, m, s = floatToHMS(1 + (59 / 60) + (59.999999 / 3600))
	assert (h, m, s) == (2, 0, 0)


def test_jdt_to_datetime_rolls_over_to_next_day_at_24_hours():
	with patch(
		'at.core.sweHelpers.swe.revjul',
		return_value=(2025, 1, 1, 23.9999999998),
	):
		result = jdtToDateTime(0, timezone.utc)

	assert result == datetime(2025, 1, 2, 0, 0, 0, tzinfo=timezone.utc)
