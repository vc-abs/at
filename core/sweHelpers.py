from datetime import (
	datetime,
	timezone,
	timedelta,
)
import swisseph as swe
from core.constants import (
	objectProps,
	degrees,
	ayanamsaSWEConstants,
)

minutesPerHor = 60
secondsPerHour = 3600
secondsPerMinute = 60
floatingPointPrecisionCorrectionSeconds = 0.001

riseFlags = (
	swe.CALC_RISE | swe.BIT_HINDU_RISING
)
setFlags = (
	swe.CALC_SET | swe.BIT_HINDU_RISING
)

gregflag = swe.GREG_CAL
# pressure & temperature or irrelevant for hindu method, can be set to 0
atmo = (1013.25, 15)
altitude = 0.0
SUN = swe.SUN

utcTimeZone = timezone(
	offset=timedelta(
		hours=0,
		minutes=0,
	)
)


def floatToHMS(floatHours):
	hours = int(floatHours)
	remainingHours = floatHours - hours
	remainingMinutes = (
		remainingHours * minutesPerHor
	)
	minutes = int(remainingMinutes)
	minutesFraction = (
		remainingMinutes
	) - minutes
	# #TODO: Fix the following bug: Floating point correction sometimes make the value exceed 59 and breaks the run.
	seconds = int(
		minutesFraction * secondsPerMinute
		+ floatingPointPrecisionCorrectionSeconds
	)

	return hours, minutes, seconds


def jdtToDateTime(
	fromTret, fromTZInfo=utcTimeZone
):
	year, month, day, floatHour = (
		swe.revjul(fromTret, gregflag)
	)

	hour, min, sec = floatToHMS(floatHour)

	return datetime(
		year,
		month,
		day,
		hour,
		min,
		sec,
		tzinfo=utcTimeZone,
	).astimezone(fromTZInfo)


def dateTimeToJDT(fromValue):
	offsetSeconds = (
		fromValue.utcoffset()
		or datetime.now(
			utcTimeZone
		).utcoffset()
	).seconds
	return swe.julday(
		fromValue.year,
		fromValue.month,
		fromValue.day,
		fromValue.hour
		+ (
			(
				fromValue.minute
				* secondsPerMinute
				+ fromValue.second
				- offsetSeconds
				+ floatingPointPrecisionCorrectionSeconds
			)
			/ secondsPerHour
		),
	)


# #Note: Precision of JDT is more than that of eventTime configuration, which is at the second level. This creates issues in computing rise and set times and is fixed by neglecting tiny differences.
def isJDTGreater(baseJDT, comparedJDT):
	isDifferenceTiny = (
		abs(baseJDT - comparedJDT) < 0.00001
	)

	return (
		False
		if isDifferenceTiny
		else baseJDT > comparedJDT
	)


def getNextRise(tjd, geopos):
	isRiseMissing, tRise = swe.rise_trans(
		tjd,
		SUN,
		riseFlags,
		geopos,
		atmo[0],
		atmo[1],
	)

	return (
		None if isRiseMissing else tRise[0]
	)


# #NOTE: There's some one minute difference in both sunrise and sunset times, when compared to JH. The flags used are to get closer to those values, and are not from proper understanding.
# #FROM: https://astrorigin.com/pyswisseph/sphinx/programmers_manual/planetary_phenomena/risings_settings_meridian_transits.html?highlight=bit_hindu_rising
def getRiseAndSetTimes(config):
	eventTime, latitude, longitude = (
		config['datetime'],
		config['latitude'],
		config['longitude'],
	)
	geopos = (
		longitude,
		latitude,
		altitude,
	)

	tjd = swe.julday(
		eventTime.year,
		eventTime.month,
		eventTime.day,
		0,
		gregflag,
	)
	eventTimeJulian = dateTimeToJDT(
		eventTime
	)
	tjd = tjd - (longitude / 360.0)
	tThisRise = getNextRise(tjd, geopos)
	direction = tThisRise and (
		-1
		if isJDTGreater(
			tThisRise, eventTimeJulian
		)
		else 1
	)
	offset = (
		1.999 if direction < 0 else 0.001
	) * direction

	tOtherRise = (
		None
		if tThisRise is None
		else getNextRise(
			tThisRise + offset,
			geopos,
		)
	)

	tRise = (
		tThisRise
		if direction > 0
		else tOtherRise
	)
	tNextRise = (
		tOtherRise
		if direction > 0
		else tThisRise
	)

	isSetMissing, tSet = swe.rise_trans(
		tRise,
		SUN,
		setFlags,
		geopos,
		atmo[0],
		atmo[1],
	)

	return {
		'sunrise': None
		if tRise is None
		else jdtToDateTime(
			tRise, eventTime.tzinfo
		),
		'sunset': None
		if isSetMissing
		else jdtToDateTime(
			tSet[0], eventTime.tzinfo
		),
		'nextRise': None
		if not tNextRise
		else jdtToDateTime(
			tNextRise, eventTime.tzinfo
		),
	}


def setAyanamsa(ayanamsa):
	swe.set_sid_mode(
		ayanamsaSWEConstants[ayanamsa],
		0,
		0,
	)


def getAyanamsaOffset(eventTime):
	eventTimeJD = dateTimeToJDT(eventTime)

	return swe.get_ayanamsa_ex(
		eventTimeJD, 0
	)[1]


def unsetAyanamsa():
	swe.close()


# #NOTE: This function is not actively used, but was kept as it seems useful and it incurred quite a chunk of effort.
def getSolarCrossingTime(
	longitude, startDate
):
	jdStartDate = dateTimeToJDT(startDate)

	jdCross = swe.solcross(
		longitude,
		jdStartDate,
		swe.FLG_SIDEREAL
		| swe.FLG_CENTER_BODY,
	)
	return jdtToDateTime(
		jdCross,
		startDate.tzinfo or utcTimeZone,
	)


def getPlanetPosition(
	planet, eventTime
):
	return swe.calc_ut(
		eventTime,
		objectProps[planet]['sweID'],
		swe.FLG_SIDEREAL,
	)[0][0]


def getPlanetMeanLongitudeAndDifference(
	planet,
	eventTime,
	avgSampleDays=365000,
):
	planetProps = objectProps[planet]
	planetMeanSpeed = planetProps[
		'meanSpeed'
	]
	eventTime = dateTimeToJDT(eventTime)
	sampleStartTime = (
		eventTime - avgSampleDays
	)

	eventLongitude = getPlanetPosition(
		planet, eventTime
	)
	sampleStartLongitude = (
		getPlanetPosition(
			planet, sampleStartTime
		)
	)
	meanLongitude = (
		sampleStartLongitude
		+ planetMeanSpeed
		* (eventTime - sampleStartTime)
	) % degrees
	difference = (
		eventLongitude - meanLongitude
	)

	return (
		meanLongitude,
		difference,
	)
