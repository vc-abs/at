# #NOTE: This method of calculation is not used as changing the anchor date impacts the calculations, quite significantly.

import sys
from pathlib import Path

sys.path.append(
	str(Path(__file__).parent.parent)
)

import swisseph as swe
from datetime import datetime
from core.sweHelpers import (
	getPlanetMeanLongitudeAndDifference,
	dateTimeToJDT,
)

chestaAnchor = dateTimeToJDT(
	datetime(1900, 1, 1)
)


def getPlanetChesta(
	planet, sunMeanLongitude, eventTime
):
	planetMeanLongitude, differece = (
		getPlanetMeanLongitudeAndDifference(
			planet,
			eventTime,
		)
	)
	planetTrueLongitude = (
		planetMeanLongitude + differece
	)
	isInnerPlanet = planet in innerPlanets

	planetMeanLongitude = (
		sunMeanLongitude
		if isInnerPlanet
		else planetMeanLongitude
	)
	seegrachaa = (
		planetMeanLongitude
		if isInnerPlanet
		else sunMeanLongitude
	)

	chestaKendra = (
		abs(
			(
				seegrachaa
				- (
					planetMeanLongitude
					+ planetTrueLongitude
				)
				/ 2
			)
		)
		% 180
	)

	return chestaKendra / 3


innerPlanets = ['mercury', 'venus']
planetOrder = [
	'mars',
	'mercury',
	'jupiter',
	'venus',
	'saturn',
]

print(chestaAnchor)


def getChestaBala(eventConfig):
	eventTime = eventConfig['datetime']
	sunMeanLongitude, _ = (
		getPlanetMeanLongitudeAndDifference(
			'sun',
			eventTime,
			dateTimeToJDT(eventTime)
			- chestaAnchor,
		)
	)

	return {
		planet: getPlanetChesta(
			planet,
			sunMeanLongitude,
			eventTime,
		)
		for planet in planetOrder
	}


def main():
	swe.set_sid_mode(swe.SIDM_RAMAN, 0, 0)
	eventTime = datetime(2000, 1, 1)

	eventConfig = {
		'ayanamsa': 'raman',
		'datetime': eventTime,
		'latitude': 9.933,
		'longitude': 78.816,
	}

	print(getChestaBala(eventConfig))


if __name__ == '__main__':
	main()
