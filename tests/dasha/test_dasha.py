from datetime import datetime, timezone

from at.dasha import Dasha, get_antar_dasha


class _panchang:
	def __init__(self, nakshatra_number):
		self.nakshatra_number = nakshatra_number


class _chart:
	def __init__(self):
		self.config = {
			'datetime': datetime(
				2025, 1, 1, tzinfo=timezone.utc
			)
		}
		# moon at start of Ashwini-ish segment for stable assertions
		self.objects = {
			'moon': {'longitude': 0.1},
		}
		self.panchang = _panchang(1)


def test_get_antar_dasha_returns_requested_prefixes():
	start = datetime(2025, 1, 1, tzinfo=timezone.utc)
	result = get_antar_dasha(
		starting_planet='jupiter',
		super_dasha_starts_at=start,
		super_dasha_length=16,
		covered_fraction=0.1,
		current_antar_dasha_depth=3,
	)

	assert set(result.keys()) == {
		'ad',
		'pad',
		'skd',
		'prd',
	}
	for key in ['ad', 'pad', 'skd', 'prd']:
		assert set(result[key].keys()) == {
			'lord',
			'startsAt',
			'endsAt',
			'remainder',
		}


def test_dasha_properties_are_computable_and_shaped():
	chart = _chart()
	dasha = Dasha(chart)

	nakshatra_lord = dasha.nakshatra_lord
	assert 'nakshatraLord' in nakshatra_lord

	maha = dasha.maha_dasha
	assert set(maha.keys()) == {
		'lord',
		'startsAt',
		'endsAt',
		'remainder',
	}
	assert 0 <= maha['remainder'] <= 1

	all_dashas = dasha.dashas
	assert len(all_dashas) == 9
	assert all_dashas[0]['lord'] == maha['lord']
	assert all_dashas[1]['startsAt'] == all_dashas[0]['endsAt']

	antar = dasha.antar_dashas
	assert set(antar.keys()) == {
		'ad',
		'pad',
		'skd',
		'prd',
	}
