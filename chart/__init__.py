from ashtakavarga import getAshtakavarga
from panchang import Panchang
from dasha import Dasha
from shadBala import ShadBala
from varga import Varga
from core.constants import (
	objects,
	signWidth,
)
from core.helpers import (
	selectObjects,
)
from core.planetaryPositions import (
	getPlanetaryPositions,
)
from core.karakas import getKarakas
from core.sweHelpers import (
	setAyanamsa,
	getAyanamsaOffset,
)
from core.Cached import Cached


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
