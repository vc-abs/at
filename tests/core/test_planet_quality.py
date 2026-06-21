from at.core.planetQuality import (
	getMercuryQuality,
	getObjectsConjunctors,
	getPlanetQuality,
)


class _Chart:
	def __init__(self, objects):
		self.objects = objects


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


def test_get_mercury_quality_from_conjunctors():
	objects = {
		'mercury': {
			'name': 'mercury',
			'house': 1,
			'type': 'planet',
			'longitude': 30,
		},
		'sun': {
			'name': 'sun',
			'house': 1,
			'type': 'planet',
			'longitude': 40,
		},
		'mars': {
			'name': 'mars',
			'house': 1,
			'type': 'planet',
			'longitude': 60,
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
	# sun is malefic (-1), mars is malefic (-1) => sign(-2) = -1
	assert getMercuryQuality(chart) == -1


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
	chart = _Chart(objects)

	assert (
		getPlanetQuality(objects['sun'], chart)
		== 'malefic'
	)
	# moon far from sun => benefic
	assert (
		getPlanetQuality(objects['moon'], chart)
		== 'benefic'
	)
	# mercury conjunct venus(benefic) => benefic
	assert (
		getPlanetQuality(
			objects['mercury'], chart
		)
		== 'benefic'
	)
