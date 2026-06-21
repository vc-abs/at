from at.ashtakavarga import getAshtakavarga
from at.panchang import Panchang
from at.dasha import Dasha
from at.shadBala import ShadBala
from at.varga import Varga
from at.core.planetaryPositions import (
	getPlanetaryPositions,
)
from at.core.karakas import getKarakas
from at.core.sweHelpers import (
	setAyanamsa,
	getAyanamsaOffset,
)
from at.core.Cached import Cached


class Chart(Cached):
	def __init__(self, config):
		super().__init__()
		self._config = config
		self.__cache__ = {
			'config': config,
		}
		setAyanamsa(config['ayanamsa'])

	def _getObjects(self):
		return getPlanetaryPositions(
			self.config
		)

	def _getAshtakavarga(self):
		return getAshtakavarga(self.objects)

	def _getAyanamsa(self):
		return {
			'name': self.config['ayanamsa'],
			'offset': getAyanamsaOffset(
				self.config['datetime']
			),
		}

	def _getPanchang(self):
		return Panchang(self)

	def _getDasha(self):
		return Dasha(self)

	def _getShadBala(self):
		return ShadBala(self)

	def _getVarga(self):
		return Varga(self)

	def _getKarakas(self):
		return getKarakas(self)


__all__ = [Chart]
