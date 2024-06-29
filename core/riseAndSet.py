import swisseph as swe
from datetime import (
	datetime,
	timezone,
	timedelta,
)

gregflag = swe.GREG_CAL
# pressure & temperature or irrelevant for hindu method, can be set to 0
atmo = (1013.25, 15)
planet = swe.SUN


def floatToHMS(floatHours):
	hours = int(floatHours)
	remainingHours = floatHours - hours
	minutes = int(remainingHours * 60)
	remainingMinutes = (
		remainingHours * 60
	) - minutes
	seconds = int(remainingMinutes * 60)

	return hours, minutes, seconds


def parseSweTime(tret, tzinfo):
	year, month, day, floatHour = (
		swe.revjul(tret[0], gregflag)
	)

	hour, min, sec = floatToHMS(floatHour)
	return datetime(
		year,
		month,
		day,
		hour,
		min,
		sec,
		tzinfo=timezone(
			offset=timedelta(
				hours=0,
				minutes=0,
			)
		),
	).astimezone(tzinfo)


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
		else parseSweTime(tRise, dt.tzinfo),
		'sunset': None
		if isSetMissing
		else parseSweTime(tSet, dt.tzinfo),
	}
