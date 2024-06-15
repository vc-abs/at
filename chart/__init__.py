from sideralib import (
	astrochart,
	astrodata,
)

from ashtakavarga import getAshtakavarga
from panchang import Panchang
from dasha import Dasha
from core.constants import (
	objects,
	signWidth,
)
from core.helpers import (
	selectObjects,
	fold,
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


def getChart(config):
	astroChart = astrodata.AstroData(
		config['year'],
		config['month'],
		config['day'],
		config['hour'],
		config['minute'],
		config['second'],
		config['utcHour'],
		config['utcMinute'],
		config['latitude'],
		config['longitude'],
		ayanamsa=config['ayanamsa'],
	)
	planetData = (
		astroChart.planets_rashi()
	)
	kundli = astrochart.Chart(
		planetData
	).lagnaChart()

	houses = [
		formatHouse(houseNum + 1, house)
		for houseNum, house in enumerate(
			kundli
		)
	]

	addAscendant(kundli, houses)

	return {'houses': houses}


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


# #NOTE: This wil not work with multi-threading.
cache = {'zeroHourChart': None}

zeroHour = dict(
	hour=0,
	minute=0,
	second=0,
)


def isZeroChartCached(config):
	return getattr(
		cache['zeroHourChart'],
		'_config',
		{'date': None},
	)['date'] == config['date'].replace(
		**zeroHour,
		microsecond=0,
	)


def getZeroChart(config):
	cache['zeroHourChart'] = (
		cache['zeroHourChart']
		if isZeroChartCached(config)
		else Chart({**config, **zeroHour})
	)
	return cache['zeroHourChart']


class Chart(Cached):
	def __init__(self, config):
		super().__init__()
		self._config = config
		self.__cache__ = {
			**getChart(config),
			'config': config,
		}

	def _getZeroHourChart(self):
		return getZeroChart(self._config)

	def _getObjects(self):
		return fold(
			[
				object
				for house in self.houses
				for object in getObjectsFromHouse(
					house
				)
			]
		)

	def _getAshtakavarga(self):
		return getAshtakavarga(self.objects)

	def _getPanchang(self):
		return Panchang(self)

	def _getDasha(self):
		return Dasha(self)


__all__ = [Chart]
