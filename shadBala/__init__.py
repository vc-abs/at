from math import fabs
from core.Cached import Cached
from core.constants import (
	planets,
	planetaryProps,
	degrees,
)

balaDefaultMaxScore = 60
balaDefaultMinScore = 0
maxDistanceBetweenPoints = degrees / 2
ucchaBalaScaleFactor = (
	maxDistanceBetweenPoints
	/ balaDefaultMaxScore
)


def calculateUcchaBala(planet):
	distanceToExaltation = fabs(
		planet['longitude']
		- planetaryProps[planet['name']][
			'exaltation'
		]
	)
	distanceToDebilitation = fabs(
		planet['longitude']
		- planetaryProps[planet['name']][
			'debilitation'
		]
	)

	return (
		balaDefaultMaxScore
		- (
			distanceToExaltation
			/ ucchaBalaScaleFactor
		)
		if (
			distanceToExaltation
			< distanceToDebilitation
		)
		else balaDefaultMinScore
		+ (
			distanceToDebilitation
			/ ucchaBalaScaleFactor
		)
	)


def calculateSaptavargajaBala(planet):
	return 0


def calculateOjaYugmaBala(planet):
	return 0


def calculateKendradiBala(planet):
	return 0


def calculateDrekkanaBala(planet):
	return 0


def calculateSthanaBala(planet):
	return (
		calculateUcchaBala(planet)
		+ calculateSaptavargajaBala(planet)
		+ calculateOjaYugmaBala(planet)
		+ calculateKendradiBala(planet)
		+ calculateDrekkanaBala(planet)
	)


def calculateDigBala(planet):
	return 0


def calculateNatonnataBala(planet):
	return 0


def calculatePakshaBala(planet):
	return 0


def calculateTribaghaBala(planet):
	return 0


def calculateAbdaBala(planet):
	return 0


def calculateMaasaBala(planet):
	return 0


def calculateVaaraBala(planet):
	return 0


def calculateHoraBala(planet):
	return 0


def calculateAyanaBala(planet):
	return 0


def calculateYuddhaBala(planet):
	return 0


def calculateKaalaBala(planet):
	return (
		calculateNatonnataBala(planet)
		+ calculateNatonnataBala(planet)
		+ calculatePakshaBala(planet)
		+ calculateTribaghaBala(planet)
		+ calculateAbdaBala(planet)
		+ calculateMaasaBala(planet)
		+ calculateVaaraBala(planet)
		+ calculateHoraBala(planet)
		+ calculateAyanaBala(planet)
		+ calculateYuddhaBala(planet)
	)


def calculateCheshtaBala(planet):
	return (
		balaDefaultMaxScore
		if not planet['retrograde']
		else balaDefaultMinScore
	)


def calculateDrikBala(planet):
	return 0


def calculateNaisargikaBala(
	planet, config
):
	return 0


def calculateShadbala(
	planet,
	config,
):
	return (
		calculateSthanaBala(planet)
		+ calculateCheshtaBala(planet)
		+ calculateDrikBala(planet)
		+ calculateNaisargikaBala(
			planet, config
		)
	)


def calculateIshtaPhala(shadbala):
	ishtaPhala = (shadbala - 1) / 2
	return ishtaPhala


def calculateKashtaPhala(shadbala):
	kashtaPhala = (shadbala + 1) / 2
	return kashtaPhala


class ShadBala(Cached):
	def __init__(self, chart):
		super().__init__()
		self._chart = chart

	def _getPhalas(self):
		planetPhalas = {}
		for planet in planets:
			shadbala = calculateShadbala(
				self._chart.objects[planet],
				self._chart.config,
			)
			ishtaPhala = calculateIshtaPhala(
				shadbala
			)
			kashtaPhala = (
				calculateKashtaPhala(shadbala)
			)
			planetPhalas[planet] = {
				'shadbala': shadbala,
				'ishtaPhala': ishtaPhala,
				'kashtaPhala': kashtaPhala,
			}

		return planetPhalas
