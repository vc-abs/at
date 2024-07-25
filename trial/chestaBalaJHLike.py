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

cheshtaAnchor = dateTimeToJDT(
	datetime(1900, 1, 1)
)


def getPlanetCheshta(
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

	cheshtaKendra = (
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

	return cheshtaKendra / 3


innerPlanets = ['mercury', 'venus']
planetOrder = [
	'mars',
	'mercury',
	'jupiter',
	'venus',
	'saturn',
]

print(cheshtaAnchor)


def getCheshtaBala(eventConfig):
	eventTime = eventConfig['datetime']
	sunMeanLongitude, _ = (
		getPlanetMeanLongitudeAndDifference(
			'sun',
			eventTime,
			dateTimeToJDT(eventTime)
			- cheshtaAnchor,
		)
	)

	return {
		planet: getPlanetCheshta(
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

	print(getCheshtaBala(eventConfig))


if __name__ == '__main__':
	main()
