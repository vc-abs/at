import swisseph as swe
from at.core.constants import (
	max_possible_distance,
	sign_count,
	sign_width,
	degrees,
	object_i_ds,
)
from at.core.helpers import (
	normalize_circular_value,
	get_sign_from_longitude,
)
from at.core.swe_helpers import (
	date_time_to_jdt,
)

planet_position_flags = (
	swe.FLG_SWIEPH
	+ swe.FLG_SPEED
	+ swe.FLG_SIDEREAL
)

house_method_alcabitus = b'B'


def get_planet_position(
	jd, planet, ascendant_sign
):
	xx, ret = swe.calc_ut(
		jd,
		object_i_ds[planet],
		planet_position_flags,
	)
	longitude = xx[0]
	speed = xx[3]
	retrograde = speed < 0
	sign = get_sign_from_longitude(longitude)
	return {
		'name': planet,
		'type': 'planet',
		'speed': speed,
		'retrograde': retrograde,
		'longitude': longitude,
		'sign': sign,
		'house': normalize_circular_value(
			sign - ascendant_sign + 1,
			sign_count,
		),
	}


def get_planetary_positions(
	config,
):
	jd = date_time_to_jdt(config['datetime'])
	_, ascmc = swe.houses_ex(
		jd,
		config['latitude'],
		config['longitude'],
		house_method_alcabitus,
		planet_position_flags,
	)
	ascendant_longitude = ascmc[0]
	ascendant_sign = get_sign_from_longitude(
		ascendant_longitude
	)
	positions = {
		'asc': {
			'name': 'asc',
			'type': 'angle',
			'longitude': ascendant_longitude,
			'sign': ascendant_sign,
			'house': 1,
		},
		**{
			planet: get_planet_position(
				jd, planet, ascendant_sign
			)
			for planet in object_i_ds
		},
	}

	rahu = positions['rahu']
	ketu_longitude = (
		normalize_circular_value(
			swe.degnorm(
				rahu['longitude']
				+ max_possible_distance
			),
			degrees,
		)
	)
	positions['ketu'] = {
		**rahu,
		'name': 'ketu',
		'sign': get_sign_from_longitude(
			ketu_longitude
		),
		'longitude': ketu_longitude,
		'house': normalize_circular_value(
			rahu['house']
			+ int(
				max_possible_distance / sign_width
			),
			sign_count,
		),
	}

	swe.close()
	return positions
