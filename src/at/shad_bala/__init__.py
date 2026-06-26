import datetime
from math import sqrt
from datetime import (
	timezone,
	timedelta,
)
from at.core.cached import Cached
from at.core.constants import (
	planets,
	object_props,
	degrees,
	kendradi_bala,
	sign_count,
	sign_width,
	max_possible_distance,
)
from at.core.helpers import (
	get_house_quality,
	get_distance_in_circle,
	get_shortest_distance_in_circle,
)
from at.core.dignity import (
	get_planet_dignity,
)
from at.core.varga import get_varga_position
from at.core.planet_quality import (
	get_planet_quality,
)
from .cheshta_bala import (
	calculate_cheshta_bala,
)

bala_default_max_score = 60
bala_default_min_score = 0
bala_default_mid_score = (
	bala_default_max_score
	- bala_default_min_score
) / 2
distance_to_score_factor = (
	bala_default_max_score
	/ max_possible_distance
)
uccha_bala_scale_factor = (
	max_possible_distance
	/ bala_default_max_score
)


def calculate_uccha_bala(planet):
	distance_to_exaltation = (
		get_shortest_distance_in_circle(
			planet['longitude'],
			object_props[planet['name']][
				'exaltation'
			],
		)
	)
	distance_to_debilitation = (
		get_shortest_distance_in_circle(
			planet['longitude'],
			object_props[planet['name']][
				'debilitation'
			],
		)
	)

	return (
		bala_default_max_score
		- (
			distance_to_exaltation
			/ uccha_bala_scale_factor
		)
		if (
			distance_to_exaltation
			< distance_to_debilitation
		)
		else bala_default_min_score
		+ (
			distance_to_debilitation
			/ uccha_bala_scale_factor
		)
	)


saptavargaja_dignity_points = {
	'own': 30,
	'greatFriend': 22.5,
	'friend': 15,
	'neutral': 7.5,
	'enemy': 3.75,
	'greatEnemy': 1.875,
}

saptavargaja_vargas = [
	1,
	2,
	3,
	9,
	7,
	12,
	30,
]


def calculate_saptavargaja_bala(
	planet, chart
):
	total = 0

	for varga in saptavargaja_vargas:
		varga_planet = get_varga_position(
			planet, varga
		)

		dignity = get_planet_dignity(
			chart=chart,
			planet=varga_planet,
		)

		total += saptavargaja_dignity_points[
			dignity
		]

	return total


oja_yugma_vargas = [1, 9]


def calculate_oja_yugma_for_varga(
	planet, varga
):
	varga_position = get_varga_position(
		planet, varga
	)
	varga_planet = {
		**planet,
		**varga_position,
	}
	return object_props[
		varga_planet['name']
	]['ojaYugmaBala'][
		1 - (varga_planet['sign'] % 2)
	]


def calculate_oja_yugma_bala(planet):
	bala = 0

	for varga in oja_yugma_vargas:
		bala += calculate_oja_yugma_for_varga(
			planet, varga
		)

	return bala


def calculate_kendradi_bala(planet):
	return kendradi_bala[
		get_house_quality(planet['house'])
	]


# #FROM: https://sacred-astrology.blogspot.com/2008/03/shadBala-and-its-conceptual-details.html
drekkana_positions = [
	'male',
	'neutral',
	'female',
]
drekkana_points = 15
drekkana_width = int(sign_width / 3)


def calculate_drekkana_bala(planet):
	drekkana = int(
		(planet['longitude']) % sign_width
	) // (drekkana_width)

	return (
		drekkana_points
		if drekkana_positions[drekkana]
		== object_props[planet['name']][
			'gender'
		]
		else 0
	)


def calculate_sthana_bala(planet, chart):
	return {
		'ucchaBala': calculate_uccha_bala(
			planet
		),
		'saptavargajaBala': calculate_saptavargaja_bala(
			planet, chart
		),
		'ojaYugmaBala': calculate_oja_yugma_bala(
			planet
		),
		'kendradiBala': calculate_kendradi_bala(
			planet
		),
		'drekkanaBala': calculate_drekkana_bala(
			planet
		),
	}


# #NOTE: BPHS-oriented Dig Bala is treated here as a linear falloff from the
# directional-strength house longitude to the opposite point. JA comparisons
# remain manual reference checks outside this implementation.
def get_dig_bala_reference_longitude(planet, chart):
	full_dig_bala_house = object_props[
		planet['name']
	]['digBalaHouse']

	return (
		chart.objects['asc']['longitude']
		+ (full_dig_bala_house - 1) * sign_width
	) % degrees



def calculate_dig_bala(planet, chart):
	distance = get_shortest_distance_in_circle(
		planet['longitude'],
		get_dig_bala_reference_longitude(
			planet, chart
		),
	)

	return (
		max_possible_distance - distance
	) * distance_to_score_factor


natonnata_tod_value_maps = {
	'day': {
		'startTime': 'sunrise',
		'endTime': 'sunset',
		'otherTOD': 'night',
	},
	'night': {
		'startTime': 'sunset',
		'endTime': 'nextRise',
		'otherTOD': 'day',
	},
}


def get_natonnata_bala_tod_values(chart):
	event_time = chart.config['datetime']
	rise_and_set = chart.panchang.rise_and_set
	tod = chart.panchang.tod
	natonnata_tod_value_map = (
		natonnata_tod_value_maps[tod]
	)
	tod_duration = (
		rise_and_set[
			natonnata_tod_value_map['endTime']
		]
		- rise_and_set[
			natonnata_tod_value_map['startTime']
		]
	).total_seconds()
	tod_elapsed = (
		event_time
		- rise_and_set[
			natonnata_tod_value_map['startTime']
		]
	).total_seconds()

	tod_bala = bala_default_max_score * (
		1
		- abs(tod_duration / 2 - tod_elapsed)
		/ tod_duration
	)

	return {
		'both': bala_default_max_score,
		f'{tod}': tod_bala,
		f'{natonnata_tod_value_map["otherTOD"]}': bala_default_max_score
		- tod_bala,
	}


def calculate_natonnata_bala(
	planet, kaala_values
):
	return kaala_values[
		'natonnataBalaTODValues'
	][object_props[planet['name']]['tod']]


def calculate_paksha_bala(planet, chart):
	paksha_bala_direction = (
		1
		if (
			planet['name'] == 'moon'
			or get_planet_quality(planet, chart)
			!= 'malefic'
		)
		else -1
	)
	objects = chart.objects
	paksha_bala_multiplier = (
		2 if planet['name'] == 'moon' else 1
	)

	sun_moon_distance = (
		get_shortest_distance_in_circle(
			objects['sun']['longitude'],
			objects['moon']['longitude'],
		)
	)
	paksha_bala_value = (
		sun_moon_distance
		* distance_to_score_factor
	)

	return (
		bala_default_min_score
		+ paksha_bala_value
		if paksha_bala_direction > 0
		else bala_default_max_score
		- paksha_bala_value
	) * paksha_bala_multiplier


tribagha_planet_order = [
	'mercury',
	'sun',
	'saturn',
	'moon',
	'venus',
	'mars',
]


tribagha_bala_points_by_planet = {
	'jupiter': bala_default_max_score,
}


def calculate_tribagha_bala(
	planet, kaala_values
):
	planet_name = planet['name']
	if planet_name in tribagha_bala_points_by_planet:
		return tribagha_bala_points_by_planet[
			planet_name
		]

	tribagha_index = int(
		kaala_values['sunToAscDistance']
		// 60
	)

	return (
		bala_default_max_score
		if tribagha_planet_order[
			tribagha_index
		]
		== planet_name
		else bala_default_min_score
	)


india_tz = timezone(
	offset=timedelta(
		hours=5,
		minutes=30,
	)
)
ahargana_anchor_date = datetime.datetime(
	2024,
	6,
	17,  # NOTE: Midnight of the previous date.
	tzinfo=india_tz,
)


def get_ahargana_days(chart):
	event_time = chart.config['datetime']
	day_offset = (
		-1
		if chart.panchang.rise_and_set[
			'sunrise'
		]
		> event_time
		else 0
	)

	return (
		event_time - ahargana_anchor_date
	).days + day_offset


bvr_abda_lord_order = [
	'moon',
	'jupiter',
	'sun',
	'mercury',
	'saturn',
	'mars',
	'venus',
]
abda_lord_count = len(bvr_abda_lord_order)
bvr_abda_year_length_in_days = 360
max_abda_bala_points = 15


def get_abda_lord_index(kaala_values):
	return (
		kaala_values['aharganaDays']
		// bvr_abda_year_length_in_days
	) % abda_lord_count



def calculate_abda_bala(
	planet, kaala_values
):
	abda_lord_index = get_abda_lord_index(
		kaala_values
	)

	return (
		bala_default_min_score
		if planet['name']
		!= bvr_abda_lord_order[abda_lord_index]
		else max_abda_bala_points
	)


bvr_maasa_lord_order = [
	'moon',
	'mercury',
	'jupiter',
	'saturn',
	'mars',
	'venus',
	'sun',
]
bvr_maasa_length_in_days = (
	bvr_abda_year_length_in_days // 12
)
max_maasa_bala_points = 30


def get_maasa_lord_index(kaala_values):
	return (
		kaala_values['aharganaDays']
		// bvr_maasa_length_in_days
	) % abda_lord_count



def calculate_maasa_bala(
	planet, kaala_values
):
	maasa_lord_index = get_maasa_lord_index(
		kaala_values
	)

	return (
		bala_default_min_score
		if planet['name']
		!= bvr_maasa_lord_order[maasa_lord_index]
		else max_maasa_bala_points
	)


max_vaara_bala_points = 45


def calculate_vaara_bala(
	planet, kaala_values
):
	return (
		max_vaara_bala_points
		if kaala_values['vaara']
		== object_props[planet['name']][
			'weekday'
		]
		else bala_default_min_score
	)


max_hora_bala_points = 60


def calculate_hora_bala(
	planet, kaala_values
):
	return (
		bala_default_min_score
		if planet['name']
		!= kaala_values['hora']
		else max_hora_bala_points
	)


# #NOTE: Ayana Bala follows a BPHS-oriented kranti-based formula here,
# using signed declination from sayana longitude and the standard planet
# groupings reflected in the companion `src/at/shad_bala/.ayana.py` sketch.
declinations_in_degrees = [
	0,
	362 / 60.0,
	703 / 60.0,
	1002 / 60.0,
	1238 / 60.0,
	1388 / 60.0,
	1440 / 60.0,
]
declination_house_width = 15
equinox_point = 180
half_equinox_point = equinox_point / 2


def calc_declination(sayana_longitude):
	bhuja = half_equinox_point - abs(
		(sayana_longitude % equinox_point)
		- half_equinox_point
	)

	dividend = int(
		bhuja // declination_house_width
	)
	remainder = (
		bhuja % declination_house_width
	)
	if dividend >= len(declinations_in_degrees) - 1:
		return declinations_in_degrees[-1]

	remaining_declination = (
		declinations_in_degrees[dividend + 1]
		- declinations_in_degrees[dividend]
	) * (
		remainder / declination_house_width
	)

	return (
		declinations_in_degrees[dividend]
		+ remaining_declination
	)


def calculate_kranti(sayana_longitude):
	declination = calc_declination(
		sayana_longitude
	)
	return (
		declination
		if 0 <= (sayana_longitude % 360) < equinox_point
		else -declination
	)


ayana_bala_kranti_adjustments = {
	'sun': lambda kranti: 24 + kranti,
	'venus': lambda kranti: 24 + kranti,
	'mars': lambda kranti: 24 + kranti,
	'jupiter': lambda kranti: 24 + kranti,
	'moon': lambda kranti: 24 - kranti,
	'saturn': lambda kranti: 24 - kranti,
	'mercury': lambda kranti: 24 + abs(kranti),
}

ayana_bala_multipliers = {
	'sun': 2,
	'moon': 1,
	'mars': 1,
	'mercury': 1,
	'jupiter': 1,
	'venus': 1,
	'saturn': 1,
}


def calculate_ayana_bala(
	planet, kaala_values
):
	ayanamsa_offset = kaala_values[
		'ayanamsaOffset'
	]
	sayana_longitude = (
		planet['longitude'] + ayanamsa_offset
	)
	kranti = calculate_kranti(
		sayana_longitude
	)
	planet_name = planet['name']
	base_bala = (
		ayana_bala_kranti_adjustments[planet_name](
			kranti
		)
		* 60
	) / 48

	return (
		base_bala
		* ayana_bala_multipliers[planet_name]
	)


planet_disc_diameters = {
	'mars': 9.4,
	'mercury': 6.6,
	'jupiter': 190.4,
	'venus': 16.6,
	'saturn': 158.0,
}

yuddha_bala_relevant_kaala_keys = {
	'natonnataBala',
	'pakshaBala',
	'tribaghaBala',
	'horaBala',
}


def get_yuddha_bala_candidates(chart):
	candidates = [
		chart.objects[planet]
		for planet in planets
		if (
			planet not in {'sun', 'moon'}
			and planet in chart.objects
		)
	]
	closest_pair = None
	closest_distance = None

	for index, left in enumerate(candidates):
		for right in candidates[index + 1 :]:
			distance = get_shortest_distance_in_circle(
				left['longitude'],
				right['longitude'],
				degrees,
			)
			if closest_distance is None or distance < closest_distance:
				closest_distance = distance
				closest_pair = (left, right)

	return closest_pair, closest_distance



def get_yuddha_bala_base_totals(chart, context, planets_in_war):
	base_totals = {}
	for planet in planets_in_war:
		kaala_bala = {
			'natonnataBala': calculate_natonnata_bala(
				planet, context['kaalaValues']
			),
			'pakshaBala': calculate_paksha_bala(
				planet, chart
			),
			'tribaghaBala': calculate_tribagha_bala(
				planet, context['kaalaValues']
			),
			'horaBala': calculate_hora_bala(
				planet, context['kaalaValues']
			),
		}
		base_totals[planet['name']] = (
			sum(
				calculate_sthana_bala(
					planet, chart
				).values()
			)
			+ calculate_dig_bala(
				planet, chart
			)
			+ sum(
				kaala_bala[key]
				for key in yuddha_bala_relevant_kaala_keys
			)
		)
	return base_totals



def calculate_yuddha_bala(planet, chart, context):
	planets_in_war, closest_distance = get_yuddha_bala_candidates(
		chart
	)
	if (
		planets_in_war is None
		or planet['name'] not in {
			planets_in_war[0]['name'],
			planets_in_war[1]['name'],
		}
	):
		return 0

	base_totals = get_yuddha_bala_base_totals(
		chart,
		context,
		planets_in_war,
	)
	left, right = planets_in_war
	base_difference = abs(
		base_totals[left['name']]
		- base_totals[right['name']]
	)
	diameter_difference = abs(
		planet_disc_diameters[left['name']]
		- planet_disc_diameters[right['name']]
	)
	yuddha_bala = (
		0
		if diameter_difference == 0
		else round(
			base_difference / diameter_difference,
			2,
		)
	)

	if planet['name'] == left['name']:
		return yuddha_bala
	return -yuddha_bala


def calculate_kaala_bala(
	planet, chart, context
):
	kaala_values = context['kaalaValues']

	return {
		'natonnataBala': calculate_natonnata_bala(
			planet, kaala_values
		),
		'pakshaBala': calculate_paksha_bala(
			planet, chart
		),
		'tribaghaBala': calculate_tribagha_bala(
			planet, kaala_values
		),
		'abdaBala': calculate_abda_bala(
			planet, kaala_values
		),
		'maasaBala': calculate_maasa_bala(
			planet, kaala_values
		),
		'vaaraBala': calculate_vaara_bala(
			planet, kaala_values
		),
		'horaBala': calculate_hora_bala(
			planet, kaala_values
		),
		'ayanaBala': calculate_ayana_bala(
			planet, kaala_values
		),
		'yuddhaBala': calculate_yuddha_bala(
			planet,
			chart,
			context,
		),
	}


drik_bala_benefics = {'moon', 'mercury', 'jupiter', 'venus'}
drik_bala_malefics = {'sun', 'mars', 'saturn'}


def calculate_drik_aspect_strength(aspecting_planet, target_planet):
	distance = get_distance_in_circle(
		aspecting_planet['longitude'],
		target_planet['longitude'],
		degrees,
	)
	planet_name = aspecting_planet['name']
	strength = 0.0

	if 30.01 <= distance <= 60.0:
		strength = 0.5 * (distance - 30.0)
	elif 60.01 <= distance <= 90.0:
		strength = (distance - 60.0) + 15
		if planet_name == 'saturn':
			strength += 45
	elif 90.01 <= distance <= 120.0:
		strength = 0.5 * (120.0 - distance) + 30
		if planet_name == 'mars':
			strength += 15
	elif 120.01 <= distance <= 150.0:
		strength = 150.0 - distance
		if planet_name == 'jupiter':
			strength += 30
	elif 150.01 <= distance <= 180.0:
		strength = 2.0 * (distance - 150.0)
	elif 180.01 <= distance <= 300.0:
		strength = 0.5 * (300.0 - distance)
		if planet_name == 'mars' and 210.01 < distance < 240.01:
			strength += 15
		if planet_name == 'jupiter' and 240.01 < distance < 270.01:
			strength += 30
		if planet_name == 'saturn' and 270.01 < distance < 300.01:
			strength += 45

	return round(strength * 0.25, 2)



def get_drik_bala_aspect_contributions(planet, chart):
	contributions = []
	for source in chart.objects.values():
		if (
			source == planet
			or source.get('type') != 'planet'
			or source['name'] not in planets
		):
			continue

		aspect_houses = object_props[
			source['name']
		].get('aspects', [])
		if get_distance_in_circle(
			source['house'],
			planet['house'],
			sign_count,
		) not in aspect_houses:
			continue

		strength = calculate_drik_aspect_strength(
			source,
			planet,
		)
		if source['name'] in drik_bala_benefics:
			contributions.append(strength)
		elif source['name'] in drik_bala_malefics:
			contributions.append(-strength)

	return contributions



def calculate_drik_bala(planet, chart):
	return round(
		sum(
			get_drik_bala_aspect_contributions(
				planet, chart
			)
		) / 4,
		2,
	)


naisargika_bala_points = {
	'sun': 60,
	'moon': 51.43,
	'mars': 17.4,
	'mercury': 25.71,
	'jupiter': 34.29,
	'venus': 42.86,
	'saturn': 8.57,
}


def calculate_naisargika_bala(planet):
	return naisargika_bala_points[
		planet['name']
	]


def calculate_shadbala(
	planet, chart, context
):
	sthana_bala = calculate_sthana_bala(
		planet, chart
	)
	kaala_bala = calculate_kaala_bala(
		planet, chart, context
	)
	other_balas = {
		'digBala': calculate_dig_bala(
			planet, chart
		),
		'cheshtaBala': calculate_cheshta_bala(
			planet, kaala_bala
		),
		'drikBala': calculate_drik_bala(
			planet, chart
		),
		'naisargikaBala': calculate_naisargika_bala(
			planet
		),
	}

	sthana_bala_total = sum(
		sthana_bala.values()
	)
	kaala_bala_total = sum(
		kaala_bala.values()
	)

	return {
		**sthana_bala,
		'sthanaBala': sthana_bala_total,
		**other_balas,
		**kaala_bala,
		'kaalaBala': kaala_bala_total,
		'shadBala': sthana_bala_total
		+ kaala_bala_total
		+ sum(other_balas.values()),
	}


def calculate_phalas(shad_bala):
	uccha_bala = shad_bala['ucchaBala']
	cheshta_bala = shad_bala['cheshtaBala']
	return {
		'ishtaPhala': sqrt(
			uccha_bala * cheshta_bala
		),
		'kashtaPhala': sqrt(
			(bala_default_max_score - uccha_bala)
			* (
				bala_default_max_score
				- cheshta_bala
			)
		),
	}


shad_bala_median_strengths = {
	'sun': 300,
	'moon': 360,
	'mars': 300,
	'mercury': 420,
	'jupiter': 390,
	'venus': 330,
	'saturn': 300,
}


def calculate_strength(planet, shad_bala):
	return {
		'strength': shad_bala['shadBala']
		/ shad_bala_median_strengths[planet]
	}


def build_context(chart):
	return {
		'kaalaValues': {
			'ayanamsaOffset': chart.ayanamsa[
				'offset'
			],
			'sunToAscDistance': (
				get_distance_in_circle(
					chart.objects['sun'][
						'longitude'
					],
					chart.objects['asc'][
						'longitude'
					],
				)
			),
			'aharganaDays': get_ahargana_days(
				chart
			),
			'vaara': chart.panchang.vaara,
			'hora': chart.panchang.hora,
			'natonnataBalaTODValues': get_natonnata_bala_tod_values(
				chart
			),
		}
	}


def calculate_planet_balas(
	planet, chart, context
):
	shad_bala = calculate_shadbala(
		chart.objects[planet],
		chart,
		context,
	)

	return {
		**shad_bala,
		**calculate_strength(
			planet, shad_bala
		),
		**calculate_phalas(shad_bala),
	}


class ShadBala(Cached):
	def __init__(self, chart):
		super().__init__()
		self._chart = chart

	def _get_balas(self):
		context = build_context(self._chart)
		return {
			planet: calculate_planet_balas(
				planet, self._chart, context
			)
			for planet in planets
		}
