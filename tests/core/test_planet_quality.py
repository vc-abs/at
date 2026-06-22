from at.core.constants import objectProps
from at.core.planetQuality import (
	getMercuryInfluencers,
	getMercuryQuality,
	getMoonQuality,
	getMoonQualityScore,
	getObjectsAspecting,
	getObjectsConjunctors,
	getPlanetQuality,
	isAspectingPlanet,
)


class _Panchang:
	def __init__(self, tithi=15):
		self.tithi = tithi


class _Chart:
	def __init__(self, objects, tithi=15):
		self.objects = objects
		self.panchang = _Panchang(tithi)


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
	chart = _Chart(objects)
	conjunctors = getObjectsConjunctors(
		chart, objects['mercury']
	)
	assert [o['name'] for o in conjunctors] == ['sun']


def test_bphs_aspect_metadata_matches_expected_values():
	assert objectProps['sun']['aspects'] == [7]
	assert objectProps['moon']['aspects'] == [7]
	assert objectProps['mars']['aspects'] == [4, 7, 8]
	assert objectProps['mercury']['aspects'] == [7]
	assert objectProps['jupiter']['aspects'] == [5, 7, 9]
	assert objectProps['venus']['aspects'] == [7]
	assert objectProps['saturn']['aspects'] == [3, 7, 10]


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

	assert isAspectingPlanet(mercury, jupiter) is True
	assert isAspectingPlanet(mercury, venus) is False


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
	chart = _Chart(objects)
	aspecting = getObjectsAspecting(chart, objects['mercury'])
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
	chart = _Chart(objects)
	influencers = getMercuryInfluencers(chart)
	assert {o['name'] for o in influencers} == {'sun', 'jupiter'}
	assert getMercuryQuality(chart) == 0


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
	chart = _Chart(objects)
	influencers = getMercuryInfluencers(chart)
	assert [o['name'] for o in influencers] == ['jupiter']
	assert getMercuryQuality(chart) == 1


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
	chart = _Chart(objects)
	assert getMercuryQuality(chart) == 0


def test_get_moon_quality_score_is_strongest_near_full_moon():
	chart = _Chart({}, tithi=15)
	near_new_chart = _Chart({}, tithi=30)

	assert getMoonQualityScore(chart) > 0
	assert getMoonQualityScore(near_new_chart) < 0
	assert getMoonQualityScore(chart) > abs(
		getMoonQualityScore(near_new_chart)
	)


def test_get_moon_quality_uses_bphs_tithi_ranges():
	assert getMoonQuality(_Chart({}, tithi=8)) == 1
	assert getMoonQuality(_Chart({}, tithi=23)) == 1
	assert getMoonQuality(_Chart({}, tithi=7)) == -1
	assert getMoonQuality(_Chart({}, tithi=24)) == -1


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
	chart = _Chart(objects, tithi=15)
	waning_chart = _Chart(objects, tithi=3)

	assert (
		getPlanetQuality(objects['sun'], chart)
		== 'malefic'
	)
	assert (
		getPlanetQuality(objects['moon'], chart)
		== 'benefic'
	)
	assert (
		getPlanetQuality(objects['moon'], waning_chart)
		== 'malefic'
	)
	# mercury conjunct venus(benefic) => benefic
	assert (
		getPlanetQuality(
			objects['mercury'], chart
		)
		== 'benefic'
	)
