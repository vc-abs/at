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
from core.sweHelpers import (
	setAyanamsa,
	getAyanamsaOffset,
)
from core.Cached import Cached


def formatPlanet(planetName, planet):
	sign = planet['lon'] // signWidth + 1
	return {
		'name': planetName,
		'type': 'planet',
		'longitude': planet['lon'],
		'retrograde': planet['retrograde'],
		'sign': sign,
	}


def formatPlanets(planets):
	return [
		formatPlanet(planetName, planet)
		for (
			planetName,
			planet,
		) in planets.items()
	]


def formatHouse(houseNum, house):
	traditionalObjects = selectObjects(
		formatPlanets(house.planets),
		objects,
	)

	return {
		'house': houseNum,
		'sign': house.sign_num,
		'objects': traditionalObjects,
	}


def addAscendant(kundli, houses):
	firstKundliHouse = kundli[0]
	houses[0]['objects'].insert(
		0,
		{
			'name': 'asc',
			'type': 'angle',
			'longitude': firstKundliHouse.asc_lon,
			'sign': firstKundliHouse.sign_num,
		},
	)


def enrichObject(object, house):
	return {
		**object,
		'sign': house['sign'],
		'house': house['house'],
	}


def getObjectsFromHouse(house):
	return [
		enrichObject(object, house)
		for object in house['objects']
	]


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


__all__ = [Chart]
