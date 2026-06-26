from at.core.constants import (
	day_rulers,
	sign_width,
)

karaka_order = [
	'ak',
	'amk',
	'bk',
	'mk',
	'pk',
	'gk',
	'dk',
]


def sort_by_degree(object):
	return sign_width - (
		object['longitude'] % sign_width
	)


def get_karakas(chart):
	filtered_objects = [
		object
		for object in chart.objects.values()
		if object['name'] in day_rulers
	]
	sorted_objects = sorted(
		filtered_objects, key=sort_by_degree
	)

	planet_names = [
		planet['name']
		for planet in sorted_objects
	]

	return {
		karakatva: planet_name
		for karakatva, planet_name in zip(
			karaka_order, planet_names
		)
	}
