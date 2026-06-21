from at.core.varga import (
	getCustomVargaPosition,
	getHoraSign,
	getOffset,
	getOffsetVargaPosition,
	getPerfectVargaPosition,
	getTrimshamsaSign,
	getVargaDegrees,
	getVargaPosition,
)


def test_hora_sign_is_computed_from_degree_bucket():
	planet = {'sign': 2, 'longitude': 35.0}
	assert getHoraSign(planet, 2) in [4, 5]


def test_trimshamsa_sign_even_and_odd_sign_rules():
	odd_sign_planet = {'sign': 1, 'longitude': 3.0}
	even_sign_planet = {'sign': 2, 'longitude': 3.0}
	assert getTrimshamsaSign(odd_sign_planet, 30) == 1
	assert getTrimshamsaSign(even_sign_planet, 30) == 2


def test_varga_degree_helpers_and_positions():
	planet = {
		'name': 'mars',
		'type': 'planet',
		'sign': 5,
		'longitude': 123.0,
	}
	longi, deg = getVargaDegrees(planet, 9)
	assert 0 <= longi < 360
	assert 0 <= deg < 30

	assert 1 <= getPerfectVargaPosition(planet, 9) <= 12
	assert 1 <= getOffsetVargaPosition(planet, 3) <= 12
	assert getCustomVargaPosition(planet, 2) in range(1, 13)


def test_get_offset_for_division_and_sign_types():
	# division varga
	assert isinstance(getOffset(3, 0, 1), int)
	# sign varga
	assert isinstance(getOffset(7, 0, 1), int)


def test_get_varga_position_returns_complete_object():
	planet = {
		'name': 'venus',
		'type': 'planet',
		'sign': 4,
		'longitude': 91.5,
	}
	pos = getVargaPosition(planet, 9)
	assert set(pos.keys()) == {
		'name',
		'type',
		'sign',
		'longitude',
		'degree',
	}
	assert pos['name'] == 'venus'
	assert 1 <= pos['sign'] <= 12
