from at.core.constants import (
	object_props,
	sign_width,
)

cheshta_bala_exceptions = {
	'sun': 'ayanaBala',
	'moon': 'pakshaBala',
}

cheshta_points = {
	'vikala': 15,
	'mandatara': 15,
	'manda': 30,
	'sama': 7.5,
	'chara': 45,
	'athiChara': 30,
	'vakra': 60,
	'anuVakra': 30,
}

sign_change_window_in_days = 3


def is_sign_changing(planet):
	current_sign_index = (
		planet['longitude'] % sign_width
	)
	future_sign_index = (
		planet['longitude']
		+ planet['speed']
		* sign_change_window_in_days
	) % sign_width

	return (
		current_sign_index != future_sign_index
	)


def get_special_planet_cheshta_bala(
	planet, kaala_bala
):
	return (
		kaala_bala[
			cheshta_bala_exceptions[
				planet['name']
			]
		]
		/ 2
	)


def get_retrograde_cheshta_bala(planet, _):
	if is_sign_changing(planet):
		speed_classification = 'vakra'
	else:
		speed_classification = 'anuVakra'

	return cheshta_points[
		speed_classification
	]


def get_general_cheshta_bala(planet, _):
	speed_increase_percent = (
		planet['speed']
		/ object_props[planet['name']][
			'meanSpeed'
		]
	) * 100

	if speed_increase_percent < 10:
		speed_classification = 'vikala'
	elif speed_increase_percent < 50:
		speed_classification = 'mandatara'
	elif speed_increase_percent < 100:
		speed_classification = 'manda'
	elif speed_increase_percent < 150:
		speed_classification = 'sama'
	elif is_sign_changing(planet):
		speed_classification = 'athiChara'
	else:
		speed_classification = 'chara'

	return cheshta_points[
		speed_classification
	]


cheshta_calculators = {
	'special': get_special_planet_cheshta_bala,
	'retro': get_retrograde_cheshta_bala,
	'general': get_general_cheshta_bala,
}


def calculate_cheshta_bala(
	planet, kaala_bala
):
	planet_name = planet['name']
	cheshta_calculator_key = (
		'special'
		if cheshta_bala_exceptions.get(
			planet_name
		)
		else (
			'retro'
			if planet['retrograde']
			else 'general'
		)
	)

	return cheshta_calculators[
		cheshta_calculator_key
	](planet, kaala_bala)
