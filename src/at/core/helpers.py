import inspect
import math
from os import path
from at.core.constants import (
	objects,
	sign_count,
	sign_width,
	degrees,
	object_props,
	house_qualities,
)


def is_traditional_object(object):
	return object['name'] in objects


def get_ordinal_position(
	cardinal_position,
	segment_count=sign_count,
):
	return math.ceil(
		cardinal_position
		/ (degrees / segment_count)
	)


def select_objects(
	items, selection=objects
):
	return list(
		filter(
			lambda item: item['name']
			in selection,
			items,
		)
	)


def fold(list_of_dicts, prop='name'):
	return {
		item[prop]: item
		for item in list_of_dicts
	}


def select(dict, keys):
	return {
		key: dict[key] for key in keys
	}


def resolve_relative_path(leaf):
	return path.join(
		path.dirname(
			inspect.stack()[1].filename
		),
		leaf,
	)


def get_planetary_quality(planet):
	return object_props[planet['name']][
		'quality'
	]


def get_house_quality(house):
	return house_qualities[(house + 2) % 3]


def normalize_circular_value(
	value, circumference
):
	return (
		value + circumference - 1
	) % circumference + 1


def get_distance_in_circle(
	p1_distance_from_start,
	p2_distance_from_start,
	circumference=degrees,
):
	return (
		circumference
		+ p2_distance_from_start
		- p1_distance_from_start
	) % circumference


def get_shortest_distance_in_circle(
	p1_distance_from_start,
	p2_distance_from_start,
	circumference=degrees,
):
	return min(
		get_distance_in_circle(
			p1_distance_from_start,
			p2_distance_from_start,
			circumference,
		),
		get_distance_in_circle(
			p2_distance_from_start,
			p1_distance_from_start,
			circumference,
		),
	)


def get_sign_distance(from_sign, to_sign):
	return (
		abs(to_sign + sign_count - from_sign)
	) % sign_count + 1


def get_sign_from_longitude(longitude):
	return int(longitude / sign_width) + 1
