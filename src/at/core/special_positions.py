from at.core.constants import (
	object_props,
)


# #TODO: Fix the exaltations for Rahu and Ketu, as they are considered to be exalted throughout the rashi.
dignity_range_in_degrees = 2


def is_in_moola_trikona(planet, *_):
	moola_trikona_start, moola_trikona_end = (
		object_props[planet['name']].get(
			'moolaTrikona',
			[0, 0],
		)
	)

	return (
		moola_trikona_start
		<= planet['longitude']
		< moola_trikona_end
	)


special_position_classifiers = {
	'exaltation': lambda planet, *_: abs(
		planet['longitude']
		- object_props[planet['name']][
			'exaltation'
		]
	)
	< dignity_range_in_degrees,
	'debilitation': lambda planet,
	*_: abs(
		planet['longitude']
		- object_props[planet['name']][
			'debilitation'
		]
	)
	< dignity_range_in_degrees,
	'moolatrikona': is_in_moola_trikona,
}


def get_planet_special_position(planet):
	for (
		special_position,
		classify,
	) in (
		special_position_classifiers.items()
	):
		if classify(planet):
			return special_position
