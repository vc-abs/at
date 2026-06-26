from at.core.constants import object_props
from at.core.planet_quality import (
	get_mercury_influencers,
	get_mercury_quality,
	get_moon_quality,
	get_moon_quality_score,
	get_objects_aspecting,
	get_objects_conjunctors,
	get_planet_quality,
	is_aspecting_planet,
)


class _panchang:
	def __init__(self, tithi=15):
		self.tithi = tithi


class _chart:
	def __init__(self, objects, tithi=15):
		self.objects = objects
		self.panchang = _panchang(tithi)


def test_get_objects_conjunctors_filters_same_house_planets_only():
	objects = {
		'mercury': {
			'name': 'mercury',
			'house': 2,
			'type': 'planet',
		},
		'sun': {'name': 'sun', 'house': 2, 'type': 'planet'},
		'moon': {'name': 'moon', 'house': 3, 'type': 'planet'},
		'asc': {'name': 'asc', 'house': 2, 'type': 'angle'},
	}
	chart = _chart(objects)
	conjunctors = get_objects_conjunctors(
		chart, objects['mercury']
	)
	assert [o['name'] for o in conjunctors] == ['sun']


def test_bphs_aspect_metadata_matches_expected_values():
	assert object_props['sun']['aspects'] == [7]
	assert object_props['moon']['aspects'] == [7]
	assert object_props['mars']['aspects'] == [4, 7, 8]
	assert object_props['mercury']['aspects'] == [7]
	assert object_props['jupiter']['aspects'] == [5, 7, 9]
	assert object_props['venus']['aspects'] == [7]
	assert object_props['saturn']['aspects'] == [3, 7, 10]


def test_is_aspecting_planet_uses_house_based_drishti():
	mercury = {
		'name': 'mercury',
		'house': 5,
		'type': 'planet',
	}
	jupiter = {
		'name': 'jupiter',
		'house': 1,
		'type': 'planet',
	}
	venus = {
		'name': 'venus',
		'house': 1,
		'type': 'planet',
	}

	assert is_aspecting_planet(mercury, jupiter) is True
	assert is_aspecting_planet(mercury, venus) is False


def test_get_objects_aspecting_filters_bphs_aspecting_planets_only():
	objects = {
		'mercury': {
			'name': 'mercury',
			'house': 5,
			'type': 'planet',
			'longitude': 150,
		},
		'jupiter': {
			'name': 'jupiter',
			'house': 1,
			'type': 'planet',
			'longitude': 15,
		},
		'venus': {
			'name': 'venus',
			'house': 1,
			'type': 'planet',
			'longitude': 18,
		},
		'rahu': {
			'name': 'rahu',
			'house': 11,
			'type': 'planet',
			'longitude': 330,
		},
		'asc': {'name': 'asc', 'house': 1, 'type': 'angle'},
	}
	chart = _chart(objects)
	aspecting = get_objects_aspecting(chart, objects['mercury'])
	assert [o['name'] for o in aspecting] == ['jupiter']


def test_get_mercury_quality_from_conjunctors_and_aspects():
	objects = {
		'mercury': {
			'name': 'mercury',
			'house': 5,
			'type': 'planet',
			'longitude': 150,
		},
		'sun': {
			'name': 'sun',
			'house': 5,
			'type': 'planet',
			'longitude': 160,
		},
		'jupiter': {
			'name': 'jupiter',
			'house': 1,
			'type': 'planet',
			'longitude': 20,
		},
		'asc': {'name': 'asc', 'house': 1, 'type': 'angle'},
		'moon': {
			'name': 'moon',
			'house': 2,
			'type': 'planet',
			'longitude': 200,
		},
	}
	chart = _chart(objects)
	influencers = get_mercury_influencers(chart)
	assert {o['name'] for o in influencers} == {'sun', 'jupiter'}
	assert get_mercury_quality(chart) == 0


def test_get_mercury_influencers_deduplicates_overlap_between_conjunction_and_aspect():
	objects = {
		'mercury': {
			'name': 'mercury',
			'house': 7,
			'type': 'planet',
			'longitude': 210,
		},
		'jupiter': {
			'name': 'jupiter',
			'house': 7,
			'type': 'planet',
			'longitude': 215,
		},
	}
	chart = _chart(objects)
	influencers = get_mercury_influencers(chart)
	assert [o['name'] for o in influencers] == ['jupiter']
	assert get_mercury_quality(chart) == 1


def test_get_mercury_quality_balances_to_neutral():
	objects = {
		'mercury': {
			'name': 'mercury',
			'house': 5,
			'type': 'planet',
			'longitude': 150,
		},
		'venus': {
			'name': 'venus',
			'house': 5,
			'type': 'planet',
			'longitude': 151,
		},
		'mars': {
			'name': 'mars',
			'house': 2,
			'type': 'planet',
			'longitude': 65,
		},
	}
	chart = _chart(objects)
	assert get_mercury_quality(chart) == 0


def test_get_moon_quality_score_is_strongest_near_full_moon():
	chart = _chart({}, tithi=15)
	near_new_chart = _chart({}, tithi=30)

	assert get_moon_quality_score(chart) > 0
	assert get_moon_quality_score(near_new_chart) < 0
	assert get_moon_quality_score(chart) > abs(
		get_moon_quality_score(near_new_chart)
	)


def test_get_moon_quality_uses_bphs_tithi_ranges():
	assert get_moon_quality(_chart({}, tithi=8)) == 1
	assert get_moon_quality(_chart({}, tithi=23)) == 1
	assert get_moon_quality(_chart({}, tithi=7)) == -1
	assert get_moon_quality(_chart({}, tithi=24)) == -1


def test_get_planet_quality_for_conditional_and_static_planets():
	objects = {
		'sun': {'name': 'sun', 'longitude': 10, 'house': 2, 'type': 'planet'},
		'moon': {'name': 'moon', 'longitude': 220, 'house': 2, 'type': 'planet'},
		'mercury': {
			'name': 'mercury',
			'longitude': 40,
			'house': 1,
			'type': 'planet',
		},
		'venus': {'name': 'venus', 'longitude': 41, 'house': 1, 'type': 'planet'},
	}
	chart = _chart(objects, tithi=15)
	waning_chart = _chart(objects, tithi=3)

	assert (
		get_planet_quality(objects['sun'], chart)
		== 'malefic'
	)
	assert (
		get_planet_quality(objects['moon'], chart)
		== 'benefic'
	)
	assert (
		get_planet_quality(objects['moon'], waning_chart)
		== 'malefic'
	)
	# mercury conjunct venus(benefic) => benefic
	assert (
		get_planet_quality(
			objects['mercury'], chart
		)
		== 'benefic'
	)
