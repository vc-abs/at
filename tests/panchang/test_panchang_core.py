from datetime import datetime, timedelta, timezone
from unittest.mock import patch

from at.panchang import Panchang, getObjectDistance


class _Chart:
	def __init__(self):
		self._config = {
			'date': datetime(
				2025, 1, 1, 8, 0, 0,
				tzinfo=timezone.utc,
			),
			'datetime': datetime(
				2025, 1, 1, 8, 0, 0,
				tzinfo=timezone.utc,
			),
		}
		self.config = self._config
		self.objects = {
			'sun': {'longitude': 10.0},
			'moon': {'longitude': 40.0},
		}


def _rise_set_stub(config):
	start = config['datetime'].replace(
		hour=6, minute=0, second=0
	)
	return {
		'sunrise': start,
		'sunset': start + timedelta(hours=12),
		'nextRise': start + timedelta(hours=24),
	}


def test_get_object_distance_wraps_correctly():
	assert (
		getObjectDistance(
			{'longitude': 350},
			{'longitude': 10},
		)
		== 20
	)


def test_panchang_core_properties_with_stubbed_rise_set():
	chart = _Chart()
	with patch(
		'at.panchang.getRiseAndSetTimes',
		side_effect=_rise_set_stub,
	):
		p = Panchang(chart)

		assert p.tithi == 3
		assert p.tod == 'day'
		assert p.vaara == 'wednesday'
		assert p.hora in [
			'sun',
			'venus',
			'mercury',
			'moon',
			'saturn',
			'jupiter',
			'mars',
		]
		assert 1 <= p.nakshatraNumber <= 27
		assert isinstance(p.nakshatra, str)
		assert 1 <= p.nakshatraPada <= 4
