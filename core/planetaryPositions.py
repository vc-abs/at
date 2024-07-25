import swisseph as swe
from core.constants import (
	maxPossibleDistance,
	signCount,
	signWidth,
	degrees,
	objectIDs,
)
from core.helpers import (
	normalizeCircularValue,
	getSignFromLongitude,
)
from core.sweHelpers import (
	dateTimeToJDT,
)

planetPositionFlags = (
	swe.FLG_SWIEPH
	+ swe.FLG_SPEED
	+ swe.FLG_SIDEREAL
)

houseMethodAlcabitus = b'B'


def getPlanetPosition(
	jd, planet, ascendantSign
):
	xx, ret = swe.calc_ut(
		jd,
		objectIDs[planet],
		planetPositionFlags,
	)
	longitude = xx[0]
	speed = xx[3]
	retrograde = speed < 0
	sign = getSignFromLongitude(longitude)
	return {
		'name': planet,
		'type': 'planet',
		'speed': speed,
		'retrograde': retrograde,
		'longitude': longitude,
		'sign': sign,
		'house': normalizeCircularValue(
			sign - ascendantSign + 1,
			signCount,
		),
	}


def getPlanetaryPositions(
	config,
):
	jd = dateTimeToJDT(config['datetime'])
	_, ascmc = swe.houses_ex(
		jd,
		config['latitude'],
		config['longitude'],
		houseMethodAlcabitus,
		planetPositionFlags,
	)
	ascendantLongitude = ascmc[0]
	ascendantSign = getSignFromLongitude(
		ascendantLongitude
	)
	positions = {
		'asc': {
			'name': 'asc',
			'type': 'angle',
			'longitude': ascendantLongitude,
			'sign': ascendantSign,
			'house': 1,
		},
		**{
			planet: getPlanetPosition(
				jd, planet, ascendantSign
			)
			for planet in objectIDs
		},
	}

	rahu = positions['rahu']
	ketuLongitude = (
		normalizeCircularValue(
			swe.degnorm(
				rahu['longitude']
				+ maxPossibleDistance
			),
			degrees,
		)
	)
	positions['ketu'] = {
		**rahu,
		'name': 'ketu',
		'sign': getSignFromLongitude(
			ketuLongitude
		),
		'longitude': ketuLongitude,
		'house': normalizeCircularValue(
			rahu['house']
			+ int(
				maxPossibleDistance / signWidth
			),
			signCount,
		),
	}

	swe.close()
	return positions
