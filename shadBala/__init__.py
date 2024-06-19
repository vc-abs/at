from math import fabs
from core.Cached import Cached
from core.constants import (
	planets,
	objectProps,
	degrees,
	kendradiBala,
	signWidth,
)
from core.helpers import (
	getPlanetaryQuality,
	getHouseQuality,
)
from core.dignity import (
	getPlanetDignity,
)
from core.varga import getVargaPosition

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
		- objectProps[planet['name']][
			'exaltation'
		]
	)
	distanceToDebilitation = fabs(
		planet['longitude']
		- objectProps[planet['name']][
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


planetDignityPoints = {
	'exaltation': 60,
	'moolatrikona': 45,
	'own': 30,
	'greatFriend': 22.5,
	'friend': 15,
	'neutral': 7.5,
	'enemy': 3.75,
	'greatEnemy': 1.875,
	'debilitation': 0,
}

saptavargajaVargas = [
	1,
	2,
	3,
	7,
	9,
	12,
	30,
]


def calculateSaptavargajaBala(planet):
	# #TODO: The calculated Saptavargaja is different than that in 'Astro App'. It looks like it's due to not considering the temporary relationship between planets. Try fixing this.
	# #NOTE: Decided to move with the imprecise calculation for now, as finding the correct methodology might not be feasible, now.
	# #NOTE: There are some minor differences between various software, Ex: between JH and Astro App.
	total = 0

	for varga in saptavargajaVargas:
		vargaPosition = getVargaPosition(
			planet, varga
		)
		total += planetDignityPoints[
			getPlanetDignity(
				{**planet, **vargaPosition}
			)
		]

	return total


def calculateOjaYugmaBala(planet):
	return objectProps[planet['name']][
		'ojaYugmaBala'
	][1 - (planet['sign'] % 2)]


# #TODO: Verify the validity of the approach. The result per JyotishApp is slightly different.
def calculateKendradiBala(planet):
	return kendradiBala[
		getHouseQuality(planet['house'])
	][getPlanetaryQuality(planet)]


# #FROM: https://sacred-astrology.blogspot.com/2008/03/shadbala-and-its-conceptual-details.html
drekkanaPositions = [
	'male',
	'neutral',
	'female',
]
drekkanaPoints = 15
drekkanaWidth = int(signWidth / 3)


def calculateDrekkanaBala(planet):
	drekkana = int(
		(planet['longitude']) % signWidth
	) // (drekkanaWidth)

	return (
		drekkanaPoints
		if drekkanaPositions[drekkana]
		== objectProps[planet['name']][
			'gender'
		]
		else 0
	)


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


def calculateDigBala(planet):
	return 0


def calculateCheshtaBala(planet):
	return (
		balaDefaultMaxScore
		if not planet['retrograde']
		else balaDefaultMinScore
	)


def calculateDrikBala(planet):
	return 0


naisargikaBalaPoints = {
	'sun': 60,
	'moon': 51,
	'mars': 32,
	'mercury': 7,
	'jupiter': 56,
	'venus': 52,
	'saturn': 5,
}


def calculateNaisargikaBala(
	planet, config
):
	return naisargikaBalaPoints[
		planet['name']
	]


def calculateShadbala(
	planet,
	config,
):
	return (
		calculateSthanaBala(planet)
		+ calculateDigBala(planet)
		+ calculateKaalaBala(planet)
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
		# #TODO: Calculate Phalas for the chart instead of separate planets, as it helps with accuracy (Ex: Calculating temporary friendships).
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
