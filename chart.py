from sideralib import (
	astrochart,
	astrodata,
)

from constants import objects, signWidth
from helpers import selectObjects
from Cached import Cached


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
	data = astrodata.AstroData(
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
	planet_data = data.planets_rashi()
	kundli = astrochart.Chart(
		planet_data
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


def getObjects(config):
	chart = getChart(config)

	return [
		object
		for house in chart['houses']
		for object in getObjectsFromHouse(
			house
		)
	]


class Chart(Cached):
	def __init__(self, config):
		self.__cache__ = {
			**self.__cache__,
			**getChart(config),
		}


__all__ = [getChart, getObjects, Chart]
