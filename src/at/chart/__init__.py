from at.ashtakavarga import get_ashtakavarga
from at.panchang import Panchang
from at.dasha import Dasha
from at.shad_bala import ShadBala
from at.varga import Varga
from at.core.planetary_positions import (
	get_planetary_positions,
)
from at.core.karakas import get_karakas
from at.core.swe_helpers import (
	set_ayanamsa,
	get_ayanamsa_offset,
)
from at.core.cached import Cached


class Chart(Cached):
	def __init__(self, config):
		super().__init__()
		self._config = config
		self.__cache__ = {
			'config': config,
		}
		set_ayanamsa(config['ayanamsa'])

	def _get_objects(self):
		return get_planetary_positions(
			self.config
		)

	def _get_ashtakavarga(self):
		return get_ashtakavarga(self.objects)

	def _get_ayanamsa(self):
		return {
			'name': self.config['ayanamsa'],
			'offset': get_ayanamsa_offset(
				self.config['datetime']
			),
		}

	def _get_panchang(self):
		return Panchang(self)

	def _get_dasha(self):
		return Dasha(self)

	def _get_shad_bala(self):
		return ShadBala(self)

	def _get_varga(self):
		return Varga(self)

	def _get_karakas(self):
		return get_karakas(self)


__all__ = [Chart]
