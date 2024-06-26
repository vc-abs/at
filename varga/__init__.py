from core.Cached import Cached
from core.varga import getVargaPosition


def getVargaPositions(varga, objects):
	return {
		key: getVargaPosition(object, varga)
		for key, object in objects.items()
	}


class Varga(Cached):
	def __init__(self, chart):
		super().__init__()
		self._chart = chart
		self.__cache__ = {}

	# #NOTE: Returning a chart instead of just positions might be better. But we are not sure how will it impact other flows like Panchang etc.
	def getVargaPositions(self, varga):
		positions = self.__cache__.get(
			varga
		) or getVargaPositions(
			varga, self._chart.objects
		)
		self.__cache__[varga] = positions

		return positions
