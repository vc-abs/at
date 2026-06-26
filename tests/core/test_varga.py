from at.core.varga import (
	get_custom_varga_position,
	get_hora_sign,
	get_offset,
	get_offset_varga_position,
	get_perfect_varga_position,
	get_trimshamsa_sign,
	get_varga_degrees,
	get_varga_position,
)


def test_hora_sign_is_computed_from_degree_bucket():
	planet = {'sign': 2, 'longitude': 35.0}
	assert get_hora_sign(planet, 2) in [4, 5]


def test_trimshamsa_sign_even_and_odd_sign_rules():
	odd_sign_planet = {'sign': 1, 'longitude': 3.0}
	even_sign_planet = {'sign': 2, 'longitude': 3.0}
	assert get_trimshamsa_sign(odd_sign_planet, 30) == 1
	assert get_trimshamsa_sign(even_sign_planet, 30) == 2


def test_varga_degree_helpers_and_positions():
	planet = {
		'name': 'mars',
		'type': 'planet',
		'sign': 5,
		'longitude': 123.0,
	}
	longi, deg = get_varga_degrees(planet, 9)
	assert 0 <= longi < 360
	assert 0 <= deg < 30

	assert 1 <= get_perfect_varga_position(planet, 9) <= 12
	assert 1 <= get_offset_varga_position(planet, 3) <= 12
	assert get_custom_varga_position(planet, 2) in range(1, 13)


def test_get_offset_for_division_and_sign_types():
	# division varga
	assert isinstance(get_offset(3, 0, 1), int)
	# sign varga
	assert isinstance(get_offset(7, 0, 1), int)


def test_get_varga_position_returns_complete_object():
	planet = {
		'name': 'venus',
		'type': 'planet',
		'sign': 4,
		'longitude': 91.5,
	}
	pos = get_varga_position(planet, 9)
	assert set(pos.keys()) == {
		'name',
		'type',
		'sign',
		'longitude',
		'degree',
	}
	assert pos['name'] == 'venus'
	assert 1 <= pos['sign'] <= 12
