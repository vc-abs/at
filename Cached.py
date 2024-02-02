class Cached:
	__cache__ = {}

	def __init__(self, config):
		self._config = config

	def __getattr__(self, attr):
		cache = self.__cache__

		if attr not in cache:
			cache[
				attr
			] = object.__getattribute__(
				self,
				'_get' + attr.capitalize(),
			)()

		return cache[attr]
