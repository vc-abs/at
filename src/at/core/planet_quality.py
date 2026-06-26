from np import sign
from at.core.constants import (
	object_props,
	nodes,
	tithi_count,
)
from at.core.helpers import get_sign_distance

planet_qualities = [
	'malefic',
	'neutral',
	'benefic',
]

quality_points = {
	'malefic': -1,
	'benefic': 1,
}


def get_objects_conjunctors(
	chart, base_planet
):
	house = base_planet['house']

	return [
		object
		for object in chart.objects.values()
		if object != base_planet
		and object['house'] == house
		and object['type'] == 'planet'
	]


def is_aspecting_planet(base_planet, influencing_planet):
	aspect_houses = object_props[
		influencing_planet['name']
	].get('aspects', [])
	return get_sign_distance(
		influencing_planet['house'],
		base_planet['house'],
	) in aspect_houses


def get_objects_aspecting(chart, base_planet):
	return [
		object
		for object in chart.objects.values()
		if object != base_planet
		and object['type'] == 'planet'
		and object['name'] not in nodes
		and is_aspecting_planet(
			base_planet,
			object,
		)
	]


def get_mercury_influencers(chart):
	mercury = chart.objects['mercury']
	influencers = {
		object['name']: object
		for object in get_objects_conjunctors(
			chart, mercury
		)
	}
	influencers.update(
		{
			object['name']: object
			for object in get_objects_aspecting(
				chart, mercury
			)
		}
	)
	return list(influencers.values())


def get_mercury_quality(chart):
	quality = 0
	for influencer in get_mercury_influencers(
		chart
	):
		quality += quality_points[
			get_planet_quality(
				influencer, chart
			)
		]
	return int(sign(quality))


moon_benefic_tithi_start = 8
moon_benefic_tithi_end = 23
moon_fullness_midpoint = 15.5
moon_max_circular_tithi_distance = tithi_count / 2


def normalize_moon_tithi(tithi):
	return tithi_count if tithi == 0 else tithi


def get_moon_quality_score(chart):
	tithi = normalize_moon_tithi(
		chart.panchang.tithi
	)
	distance_from_full_moon = min(
		abs(tithi - moon_fullness_midpoint),
		tithi_count - abs(tithi - moon_fullness_midpoint),
	)
	score = (
		moon_benefic_tithi_start
		- distance_from_full_moon
	)
	return score


def get_moon_quality(chart):
	return int(
		sign(
			get_moon_quality_score(chart)
		)
	)


conditional_qualifiers = {
	'moon': get_moon_quality,
	'mercury': get_mercury_quality,
}


def get_planet_quality(planet, chart):
	planet_name = planet['name']
	planet_quality = object_props[
		planet_name
	]['quality']
	return (
		planet_quality
		if planet_quality != 'conditional'
		else planet_qualities[
			conditional_qualifiers[planet_name](
				chart
			)
			+ 1
		]
	)
