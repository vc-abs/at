from datetime import datetime, timedelta, timezone
from unittest.mock import patch

from at.panchang import Panchang
from at.panchang.gowri import getScheduleNames


class _Chart:
	def __init__(self, event_time):
		self._config = {
			'date': event_time,
			'datetime': event_time,
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



def _make_panchang(event_time):
	chart = _Chart(event_time)
	with patch(
		'at.panchang.getRiseAndSetTimes',
		side_effect=_rise_set_stub,
	):
		panchang = Panchang(chart)
		_ = panchang.riseAndSet
		_ = panchang.vaara
		return panchang



def test_gowri_schedule_has_day_and_night_rows():
	p = _make_panchang(
		datetime(2025, 1, 5, 8, 0, 0, tzinfo=timezone.utc)
	)
	schedule = p.gowriSchedule

	assert list(schedule.keys()) == ['day', 'night']
	assert len(schedule['day']) == 8
	assert len(schedule['night']) == 8
	assert schedule['day'][0]['name'] == 'uthi'
	assert schedule['night'][0]['name'] == 'dhanam'



def test_gowri_segment_uses_day_schedule_and_boundaries():
	p = _make_panchang(
		datetime(2025, 1, 6, 7, 0, 0, tzinfo=timezone.utc)
	)
	segment = p.gowriSegment

	assert segment['name'] == 'amirdham'
	assert segment['tod'] == 'day'
	assert segment['segment'] == 1
	assert segment['score'] == 2



def test_gowri_segment_uses_night_schedule():
	p = _make_panchang(
		datetime(2025, 1, 6, 20, 0, 0, tzinfo=timezone.utc)
	)
	segment = p.gowriSegment

	assert segment['name'] == 'soram'
	assert segment['tod'] == 'night'
	assert segment['segment'] == 2
	assert segment['score'] == -1



def test_gowri_flags_are_exposed_with_compact_marker():
	p = _make_panchang(
		datetime(2025, 1, 7, 18, 30, 0, tzinfo=timezone.utc)
	)
	flags = p.gowri

	assert flags['gowri'] == 'soram'
	assert flags['gowriScore'] == -1
	assert flags['gowriT'] == 'night'
	assert flags['gowriF'] == 'night|soram'



def test_night_gowri_matches_day_gowri_of_plus_four_weekday():
	assert getScheduleNames('sunday', 'night') == getScheduleNames('thursday', 'day')
	assert getScheduleNames('monday', 'night') == getScheduleNames('friday', 'day')
	assert getScheduleNames('tuesday', 'night') == getScheduleNames('saturday', 'day')
