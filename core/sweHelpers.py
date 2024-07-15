from datetime import (
	datetime,
	timezone,
	timedelta,
)
import swisseph as swe
from sideralib import (
	astrodata,
)

gregflag = swe.GREG_CAL
# pressure & temperature or irrelevant for hindu method, can be set to 0
atmo = (1013.25, 15)
planet = swe.SUN

utcTimeZone = timezone(
	offset=timedelta(
		hours=0,
		minutes=0,
	)
)


def floatToHMS(floatHours):
	# #TODO: Fix the minor inconsistency (of 1 second), happening probably due to difference in floating point operations, when the timezone is +05:30.
	hours = int(floatHours)
	remainingHours = floatHours - hours
	minutes = int(remainingHours * 60)
	remainingMinutes = (
		remainingHours * 60
	) - minutes
	seconds = int(remainingMinutes * 60)

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
		(offsetSeconds / 3600),
	)


# #NOTE: There's some one minute difference in both sunrise and sunset times, when compared to JH. The flags used are to get closer to those values, and are not from proper understanding.
# #TODO: Fix the discrepancy in time calculation.
# #FROM: https://astrorigin.com/pyswisseph/sphinx/programmers_manual/planetary_phenomena/risings_settings_meridian_transits.html?highlight=bit_hindu_rising
def getRiseAndSetTimes(config):
	dt, latitude, longitude = (
		config['datetime'],
		config['latitude'],
		config['longitude'],
	)
	altitude = 0.0
	geopos = (
		longitude,
		latitude,
		altitude,
	)

	tjd = swe.julday(
		dt.year,
		dt.month,
		dt.day,
		0,
		gregflag,
	)

	tjd = tjd - (longitude / 360.0)

	rsmi = (
		swe.CALC_RISE | swe.BIT_DISC_CENTER
	)
	isRiseMissing, tRise = swe.rise_trans(
		tjd,
		planet,
		rsmi,
		geopos,
		atmo[0],
		atmo[1],
	)

	rsmi = (
		swe.CALC_SET | swe.BIT_HINDU_RISING
	)
	isSetMissing, tSet = swe.rise_trans(
		tjd,
		planet,
		rsmi,
		geopos,
		atmo[0],
		atmo[1],
	)

	return {
		'sunrise': None
		if isRiseMissing
		else jdtToDateTime(
			tRise[0], dt.tzinfo
		),
		'sunset': None
		if isSetMissing
		else jdtToDateTime(
			tSet[0], dt.tzinfo
		),
	}


# #NOTE: This function is not actively used, but was kept as it seems useful and it incurred quite a chunk of effort.
def getAyanamsaOffset(
	forTime=None, ayanamsaName=None
):
	forTime = forTime or datetime.now()
	swe.set_sid_mode(swe.SIDM_RAMAN, 0, 0)

	return swe.get_ayanamsa_ex(
		swe.julday(
			2024,
			1,
			1,
		),
		0,
	)[1]


# #NOTE: This function is not actively used, but was kept as it seems useful and it incurred quite a chunk of effort.
def getSolarCrossingTime(
	longitude, startDate
):
	# #TODO: Fix the following bug. The Ayanamsa is hardcoded, instead of being passed as a param, as the proper way to implement is not known (even to get the current value).
	swe.set_sid_mode(swe.SIDM_RAMAN, 0, 0)
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
