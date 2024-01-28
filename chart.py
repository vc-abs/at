from sideralib import astrochart, astrodata

from constants import signs, houseCount
from helpers import isTraditionalObject

def formatPlanet(planetName, planet):
	return {
		"name": planetName,
		"type": "planet",
		"degree": planet["signlon"],
		"retro": planet["retrograde"],
	}

def formatPlanets(planets):
	return [
		formatPlanet(planetName, planet) for (planetName, planet) in planets.items()
	]

def formatHouse(houseNum, house):
	traditionalPlanets = list(filter(isTraditionalObject, formatPlanets(house.planets)))

	return {
		"house": houseNum,
		"sign": house.sign_num,
		"objects": traditionalPlanets,
	}

def getChart(config):
	data = astrodata.AstroData(
		config["year"], config["month"], config["day"],
		config["hour"], config["minute"], config["second"],
		config["utcHour"], config["utcMinute"],
		config["latitude"], config["longitude"],
		ayanamsa=config["ayanamsa"]
	)
	planet_data = data.planets_rashi()
	kundli = astrochart.Chart(planet_data).lagnaChart()

	firstKundliHouse = kundli[0]
	houses = [formatHouse(houseNum + 1, house) for houseNum, house in enumerate(kundli)]

	houses[0]["objects"].insert(0, {
		"name": "asc",
		"type": "angle",
		"degree": firstKundliHouse.asc_signlon,
	})

	return {"houses": houses}

def enrichObject(object, house):
	return { **object, "sign": house["sign"], "house": house["house"] }

def getObjectsFromHouse(house):
	return [enrichObject(object, house) for object in house["objects"]]

def getObjects(config):
	chart = getChart(config)

	return [
		object
		for house in chart["houses"]
		for object in getObjectsFromHouse(house)
	]

__all__ = [getChart, getObjects]
