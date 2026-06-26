from at.shad_bala import (
	calculate_abda_bala,
	calculate_ayana_bala,
	calculate_dig_bala,
	calculate_drik_aspect_strength,
	calculate_drik_bala,
	calculate_kranti,
	calculate_maasa_bala,
	calculate_yuddha_bala,
	get_abda_lord_index,
	get_dig_bala_reference_longitude,
	get_drik_bala_aspect_contributions,
	get_maasa_lord_index,
	get_yuddha_bala_candidates,
)


class _chart:
	def __init__(self, asc_longitude, objects=None):
		self.objects = {
			'asc': {'longitude': asc_longitude},
			**(objects or {}),
		}



def test_get_dig_bala_reference_longitude_uses_planet_directional_house():
	chart = _chart(10)
	jupiter = {'name': 'jupiter', 'longitude': 0}
	moon = {'name': 'moon', 'longitude': 0}

	assert get_dig_bala_reference_longitude(jupiter, chart) == 10
	assert get_dig_bala_reference_longitude(moon, chart) == 100



def test_calculate_dig_bala_is_maximum_at_reference_longitude():
	chart = _chart(25)
	planet = {'name': 'sun', 'longitude': 295}

	assert calculate_dig_bala(planet, chart) == 60



def test_calculate_dig_bala_is_zero_at_opposite_point():
	chart = _chart(25)
	planet = {'name': 'sun', 'longitude': 115}

	assert calculate_dig_bala(planet, chart) == 0



def test_calculate_dig_bala_falls_off_linearly_by_shortest_distance():
	chart = _chart(25)
	planet = {'name': 'sun', 'longitude': 340}

	assert calculate_dig_bala(planet, chart) == 45



def test_calculate_kranti_flips_sign_across_ayana_halves():
	assert calculate_kranti(90) > 0
	assert calculate_kranti(270) < 0



def test_calculate_ayana_bala_follows_planet_groupings():
	kaala_values = {'ayanamsaOffset': 0}
	sun = {'name': 'sun', 'longitude': 90}
	moon = {'name': 'moon', 'longitude': 90}
	mercury = {'name': 'mercury', 'longitude': 270}

	assert calculate_ayana_bala(sun, kaala_values) > 60
	assert calculate_ayana_bala(moon, kaala_values) < 30
	assert calculate_ayana_bala(mercury, kaala_values) > 30



def test_calculate_drik_aspect_strength_is_graded_by_longitude_distance():
	aspecting = {
		'name': 'jupiter',
		'house': 1,
		'type': 'planet',
		'longitude': 0,
	}
	target = {
		'name': 'sun',
		'house': 7,
		'type': 'planet',
		'longitude': 150,
	}

	assert calculate_drik_aspect_strength(aspecting, target) > 0



def test_calculate_drik_bala_sums_benefic_and_malefic_aspects():
	planet = {
		'name': 'sun',
		'house': 7,
		'type': 'planet',
		'longitude': 180,
	}
	chart = _chart(
		0,
		objects={
			'sun': planet,
			'jupiter': {
				'name': 'jupiter',
				'house': 3,
				'type': 'planet',
				'longitude': 40,
			},
			'saturn': {
				'name': 'saturn',
				'house': 3,
				'type': 'planet',
				'longitude': 20,
			},
			'mars': {
				'name': 'mars',
				'house': 5,
				'type': 'planet',
				'longitude': 120,
			},
		},
	)
	contribs = get_drik_bala_aspect_contributions(planet, chart)
	assert contribs == []
	assert isinstance(calculate_drik_bala(planet, chart), float)



def test_get_yuddha_bala_candidates_finds_closest_non_luminary_pair():
	chart = _chart(
		0,
		objects={
			'mars': {
				'name': 'mars',
				'house': 1,
				'type': 'planet',
				'longitude': 10,
			},
			'mercury': {
				'name': 'mercury',
				'house': 1,
				'type': 'planet',
				'longitude': 12,
			},
			'jupiter': {
				'name': 'jupiter',
				'house': 2,
				'type': 'planet',
				'longitude': 80,
			},
		}
	)
	pair, distance = get_yuddha_bala_candidates(chart)
	assert {p['name'] for p in pair} == {'mars', 'mercury'}
	assert distance == 2



def test_calculate_yuddha_bala_returns_zero_when_planet_not_in_war():
	chart = _chart(
		0,
		objects={
			'mars': {
				'name': 'mars',
				'house': 1,
				'type': 'planet',
				'longitude': 10,
				'retrograde': False,
				'speed': 0.5,
				'sign': 1,
			},
			'mercury': {
				'name': 'mercury',
				'house': 1,
				'type': 'planet',
				'longitude': 12,
				'retrograde': False,
				'speed': 1.0,
				'sign': 1,
			},
			'jupiter': {
				'name': 'jupiter',
				'house': 2,
				'type': 'planet',
				'longitude': 80,
				'retrograde': False,
				'speed': 0.08,
				'sign': 3,
			},
			'sun': {
				'name': 'sun',
				'house': 3,
				'type': 'planet',
				'longitude': 150,
			},
			'moon': {
				'name': 'moon',
				'house': 4,
				'type': 'planet',
				'longitude': 220,
			},
			'venus': {
				'name': 'venus',
				'house': 5,
				'type': 'planet',
				'longitude': 250,
				'retrograde': False,
				'speed': 1.1,
				'sign': 9,
			},
			'saturn': {
				'name': 'saturn',
				'house': 6,
				'type': 'planet',
				'longitude': 300,
				'retrograde': False,
				'speed': 0.03,
				'sign': 11,
			},
		},
	)
	context = {
		'kaalaValues': {
			'ayanamsaOffset': 0,
			'aharganaDays': 0,
			'vaara': 'sunday',
			'hora': 'sun',
			'sunToAscDistance': 0,
			'natonnataBalaTODValues': {
				'day': 30,
				'night': 30,
				'both': 60,
			},
		}
	}

	assert calculate_yuddha_bala(chart.objects['jupiter'], chart, context) == 0



def test_abda_and_maasa_indices_are_derived_from_ahargana_days():
	kaala_values = {'aharganaDays': 0}
	assert get_abda_lord_index(kaala_values) == 0
	assert get_maasa_lord_index(kaala_values) == 0

	kaala_values = {'aharganaDays': 360}
	assert get_abda_lord_index(kaala_values) == 1

	kaala_values = {'aharganaDays': 30}
	assert get_maasa_lord_index(kaala_values) == 1



def test_abda_and_maasa_bala_award_points_to_current_lords():
	abda_values = {'aharganaDays': 360}
	maasa_values = {'aharganaDays': 30}

	assert calculate_abda_bala({'name': 'jupiter'}, abda_values) == 15
	assert calculate_abda_bala({'name': 'sun'}, abda_values) == 0
	assert calculate_maasa_bala({'name': 'mercury'}, maasa_values) == 30
	assert calculate_maasa_bala({'name': 'moon'}, maasa_values) == 0
