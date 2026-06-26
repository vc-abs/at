from at.core.constants import (
	planetary_friendships,
	sign_lords,
)
from at.core.helpers import (
	get_sign_distance,
)


# #NOTE: exaltation and debilitation is not considered for dignity calculation, as its not found in many references.
# #NOTE: Moolatrikona is not used, as it's not used in JH or JA.


def get_temporary_relationship_points(
	planet, dispositor
):
	sign_distance = get_sign_distance(
		planet['sign'], dispositor['sign']
	)

	return (
		1
		if (
			1 < sign_distance < 5
			or 9 < sign_distance
		)
		else -1
	)


composite_dignities = [
	'greatEnemy',
	'enemy',
	'neutral',
	'friend',
	'greatFriend',
	'own',
]


def get_dispositor_relationship(
	planet, objects
):
	dispositor_name = sign_lords[
		planet['sign']
	]
	dignity_index = (
		3
		if dispositor_name == planet['name']
		else planetary_friendships[
			(
				planet['name'],
				dispositor_name,
			)
		]
		+ get_temporary_relationship_points(
			objects[planet['name']],
			objects[dispositor_name],
		)
	) + 2

	dignity = composite_dignities[
		dignity_index
	]

	return dignity


def get_planet_dignity(chart, planet={}):
	objects = chart.objects
	return get_dispositor_relationship(
		planet, objects
	)
