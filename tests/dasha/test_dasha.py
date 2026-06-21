from datetime import datetime, timezone

from at.dasha import Dasha, getAntarDasha


class _Panchang:
	def __init__(self, nakshatra_number):
		self.nakshatraNumber = nakshatra_number


class _Chart:
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
		self.panchang = _Panchang(1)


def test_get_antar_dasha_returns_requested_prefixes():
	start = datetime(2025, 1, 1, tzinfo=timezone.utc)
	result = getAntarDasha(
		startingPlanet='jupiter',
		superDashaStartsAt=start,
		superDashaLength=16,
		coveredFraction=0.1,
		currentAntarDashaDepth=3,
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
	chart = _Chart()
	dasha = Dasha(chart)

	nakshatra_lord = dasha.nakshatraLord
	assert 'nakshatraLord' in nakshatra_lord

	maha = dasha.mahaDasha
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

	antar = dasha.antarDashas
	assert set(antar.keys()) == {
		'ad',
		'pad',
		'skd',
		'prd',
	}
