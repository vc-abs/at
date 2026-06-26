from at.core.cached import Cached
from at.core.varga import get_varga_position


def get_varga_positions(varga, objects):
	return {
		key: get_varga_position(object, varga)
		for key, object in objects.items()
	}


class Varga(Cached):
	def __init__(self, chart):
		super().__init__()
		self._chart = chart
		self.__cache__ = {}

	# #NOTE: Returning a chart instead of just positions might be better. But we are not sure how will it impact other flows like Panchang etc.
	def get_varga_positions(self, varga):
		positions = self.__cache__.get(
			varga
		) or get_varga_positions(
			varga, self._chart.objects
		)
		self.__cache__[varga] = positions

		return positions
