class Cached:
	def __init__(self):
		self.__cache__ = {}

	def __getattr__(self, attr):
		cache = self.__cache__

		if attr not in cache:
			cache[
				attr
			] = object.__getattribute__(
				self,
				'_get'
				+ attr[0].capitalize()
				+ attr[1:],
			)()

		return cache[attr]
