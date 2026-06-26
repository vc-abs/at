import pytest

from at.core import constants
from at.core.helpers import (
	normalize_circular_value,
	get_distance_in_circle,
	get_shortest_distance_in_circle,
	get_sign_distance,
	get_sign_from_longitude,
	fold,
	select,
)


def test_normalize_circular_value_basic():
	# unchanged values
	assert (
		normalize_circular_value(1, 360) == 1
	)
	assert (
		normalize_circular_value(360, 360)
		== 360
	)


def test_normalize_circular_value_wraps():
	assert (
		normalize_circular_value(361, 360)
		== 1
	)
	assert (
		normalize_circular_value(0, 360)
		== 360
	)


@pytest.mark.parametrize(
	'p1,p2,exp',
	[
		(10, 20, 10),
		(350, 10, 20),
	],
)
def test_get_distance_in_circle(
	p1, p2, exp
):
	assert (
		get_distance_in_circle(
			p1, p2, constants.degrees
		)
		== exp
	)


@pytest.mark.parametrize(
	'p1,p2,exp',
	[
		(10, 20, 10),
		(350, 10, 20),
	],
)
def test_get_shortest_distance_in_circle(
	p1, p2, exp
):
	assert (
		get_shortest_distance_in_circle(
			p1, p2, constants.degrees
		)
		== exp
	)


def test_get_sign_distance_and_from_longitude():
	# Using default sign count of 12, width 30 degrees
	# Distance from sign 1 to 12 should be 12 steps
	assert get_sign_distance(1, 12) == 12
	# Longitude boundaries
	assert get_sign_from_longitude(0) == 1
	assert (
		get_sign_from_longitude(359.9)
		== constants.sign_count
	)


def test_fold_and_select():
	items = [
		{
			'name': 'a',
			'value': 1,
			'extra': True,
		},
		{
			'name': 'b',
			'value': 2,
			'extra': False,
		},
	]
	folded = fold(items)
	assert 'a' in folded and 'b' in folded
	assert folded['a']['value'] == 1

	selected = select(
		folded['b'], ['name', 'value']
	)
	assert selected == {
		'name': 'b',
		'value': 2,
	}
