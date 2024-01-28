from sideralib import astrochart, astrodata

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
	return {
		"house": houseNum,
		"signNum": house.sign_num,
		"objects": formatPlanets(house.planets),
	}

def getChart(year, month, day, hour, minute, second, utcHour, utcMinute, latitude, longitude, ayanamsa):
	data = astrodata.AstroData(
	 year, month, day, hour, minute, second, utcHour, utcMinute,
	 latitude, longitude, ayanamsa=ayanamsa
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
