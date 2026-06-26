from at.core.constants import (
	sign_count,
	sign_width,
	degrees,
)


def get_hora_sign(planet, varga):
	degree_in_sign = (
		planet['longitude'] % sign_width
	)
	varga_position = degree_in_sign // (
		sign_width // varga
	)

	return (
		4
		+ (planet['sign'] + varga_position)
		% varga
	)


trimshamsa_rulership = [
	{
		(0, 5): 2,
		(5, 10): 6,
		(
			10,
			18,
		): 12,
		(18, 25): 10,
		(25, 30): 8,
	},
	{
		(0, 5): 1,
		(5, 10): 11,
		(
			10,
			18,
		): 9,
		(18, 25): 3,
		(25, 30): 7,
	},
]


def get_trimshamsa_sign(planet, varga):
	degree_in_sign = (
		planet['longitude'] % sign_width
	)

	for (
		(start, end),
		sign,
	) in trimshamsa_rulership[
		planet['sign'] % 2
	].items():
		if start <= degree_in_sign < end:
			return sign


varga_config = {
	1: {
		'type': 'custom',
		'fn': lambda planet, varga: planet[
			'sign'
		],
	},
	2: {
		'type': 'custom',
		'fn': get_hora_sign,
	},
	3: {
		'type': 'division',
		'offsets': [1, 5, 9],
	},
	4: {
		'type': 'division',
		'offsets': [1, 4, 7, 10],
	},
	5: {
		'type': 'division',
		'offsets': [
			1,
			11,
			9,
			3,
			7,
			2,
			6,
			12,
			10,
			8,
		],
	},
	6: {'type': 'perfect'},
	7: {
		'type': 'sign',
		'offsets': [1, 7],
	},
	8: {'type': 'perfect'},
	9: {'type': 'perfect'},
	10: {
		'type': 'sign',
		'offsets': [1, 9],
	},
	11: {'type': 'perfect'},
	12: {
		'type': 'sign',
		'offsets': [1],
	},
	16: {'type': 'perfect'},
	20: {'type': 'perfect'},
	24: {
		'type': 'sign',
		'offsets': [
			5,
			3,
			3,
			1,
			1,
			11,
			11,
			9,
			9,
			7,
			7,
			5,
		],
	},
	27: {'type': 'perfect'},
	30: {
		'type': 'custom',
		'fn': get_trimshamsa_sign,
	},
	40: {
		'type': 'sign',
		'offsets': [
			1,
			6,
			11,
			4,
			9,
			2,
			7,
			12,
			5,
			10,
			3,
			8,
		],
	},
	45: {
		'type': 'sign',
		'offsets': [1, 4, 7, 10],
	},
	60: {
		'type': 'sign',
		'offsets': [1],
	},
}


def get_varga_offset(
	offset_data, varga_position, sign
):
	return (
		offset_data['offsets'][varga_position]
		- 1
	)


def get_rashi_offset(
	offset_data, varga_position, sign
):
	offsets = offset_data['offsets']
	return (
		offsets[(sign - 1) % len(offsets)]
		- 1
		+ varga_position
	)


offset_type_processors = {
	'division': get_varga_offset,
	'sign': get_rashi_offset,
}


def get_varga_degrees(planet, varga):
	varga_longitude = (
		planet['longitude'] * varga
	) % degrees
	varga_degree = (
		varga_longitude % sign_width
	)

	return (varga_longitude, varga_degree)


def get_offset(
	varga, varga_position, sign
):
	offset_data = varga_config[varga]
	return offset_type_processors[
		offset_data['type']
	](offset_data, varga_position, sign)


def get_offset_varga_position(
	planet, varga
):
	longitude = planet['longitude']
	sign_index = planet['sign'] - 1
	degrees_within_sign = (
		longitude % sign_width
	)
	varga_width = sign_width / varga
	varga_position = int(
		degrees_within_sign // varga_width
	)
	offset = get_offset(
		varga, varga_position, planet['sign']
	)
	varga_sign = int(
		(sign_index + offset) % sign_count + 1
	)

	return varga_sign


def get_perfect_varga_position(
	planet, varga
):
	varga_longitude, varga_degree = (
		get_varga_degrees(planet, varga)
	)

	varga_sign = (
		int(varga_longitude // sign_width)
		% sign_count
	) + 1

	return varga_sign


def get_custom_varga_position(
	planet, varga
):
	sign = varga_config[varga]['fn'](
		planet, varga
	)

	return sign


varga_type_processors = {
	'perfect': get_perfect_varga_position,
	'sign': get_offset_varga_position,
	'division': get_offset_varga_position,
	'custom': get_custom_varga_position,
}


def get_varga_position(planet, varga):
	varga_type = varga_config.get(
		varga, {}
	).get('type', 'perfect')

	sign = int(
		varga_type_processors[varga_type](
			planet, varga
		)
	)
	longitude, degree = get_varga_degrees(
		planet, varga
	)

	return {
		'name': planet['name'],
		'type': planet['type'],
		'sign': sign,
		'longitude': longitude,
		'degree': degree,
	}
