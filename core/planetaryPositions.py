import swisseph as swe
from core.constants import (
	maxPossibleDistance,
	signCount,
	signWidth,
	degrees,
	objectIDs,
	ayanamsaSWEConstants,
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
		'speed': speed,
		'retrograde': retrograde,
		'longitude': longitude,
		'sign': sign,
		'house': normalizeCircularValue(
			sign - ascendantSign, signCount
		),
	}


def getPlanetaryPositions(
	config,
):
	swe.set_sid_mode(
		ayanamsaSWEConstants[
			config['ayanamsa']
		],
		0,
		0,
	)
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
		'ascendant': {
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
