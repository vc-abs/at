from at.core.dignity import (
	get_dispositor_relationship,
	get_planet_dignity,
	get_temporary_relationship_points,
)


class _chart:
	def __init__(self, objects):
		self.objects = objects


def test_temporary_relationship_points_friend_and_enemy_ranges():
	# sign distance 3 => friend (+1)
	planet = {'sign': 1}
	dispositor = {'sign': 3}
	assert get_temporary_relationship_points(planet, dispositor) == 1

	# sign distance 5 => enemy (-1)
	dispositor_enemy = {'sign': 5}
	assert (
		get_temporary_relationship_points(
			planet, dispositor_enemy
		)
		== -1
	)


def test_dispositor_relationship_own_sign_returns_own():
	planet = {'name': 'mars', 'sign': 1}
	objects = {
		'mars': {'name': 'mars', 'sign': 1},
		'sun': {'name': 'sun', 'sign': 5},
	}
	assert (
		get_dispositor_relationship(planet, objects)
		== 'own'
	)


def test_get_planet_dignity_uses_chart_objects():
	# Mars in Taurus(sign=2), dispositor Venus in Cancer(sign=4)
	# natural friendship mars->venus = 0
	# temporary relationship sign distance(2->4)=3 => +1
	# dignity index = 0 + 1 + 2 = 3 => 'friend'
	objects = {
		'mars': {'name': 'mars', 'sign': 2},
		'venus': {'name': 'venus', 'sign': 4},
	}
	chart = _chart(objects)
	planet = {'name': 'mars', 'sign': 2}
	assert get_planet_dignity(chart, planet) == 'friend'
