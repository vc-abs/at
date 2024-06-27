import swisseph as swe
from datetime import (
	datetime,
	timezone,
	timedelta,
)

gregflag = swe.GREG_CAL


def changeTimezone(
	dt_utc, offset_hours, offset_minutes
):
	# Create a timedelta object with the specified offset
	offset = timedelta(
		hours=offset_hours,
		minutes=offset_minutes,
	)

	# Apply the offset to the UTC datetime
	dt_with_offset = dt_utc + offset

	return dt_with_offset


def floatHMS(float_hours):
	hours = int(float_hours)
	remaining_hours = float_hours - hours
	minutes = int(remaining_hours * 60)
	remaining_minutes = (
		remaining_hours * 60
	) - minutes
	seconds = int(remaining_minutes * 60)

	return hours, minutes, seconds


def parseSweTime(tret):
	year, month, day, floatHour = (
		swe.revjul(tret[0], gregflag)
	)

	hour, min, sec = floatHMS(floatHour)
	return changeTimezone(
		datetime(
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
		),
		5,
		30,
	)


def getRiseAndSetTimes(
	year,
	month,
	day,
	longitude,
	latitude,
	altitude=0.0,
):
	# pressure & temperature or irrelevant for hindu method, can be set to 0
	atmo = (1013.25, 15)
	geopos = (
		longitude,
		latitude,
		altitude,
	)
	epheflag = swe.FLG_SWIEPH
	swe.set_topo(*geopos)
	pl = swe.SUN
	tjd = swe.julday(
		year, month, day, 0, gregflag
	)
	dt = longitude / 360.0
	tjd = tjd - dt

	rsmi = (
		swe.CALC_RISE
		# | swe.BIT_DISC_CENTER
		| swe.BIT_HINDU_RISING
		# | swe.BIT_NO_REFRACTION
	)
	isRiseMissing, tRise = swe.rise_trans(
		tjd,
		pl,
		rsmi,
		geopos,
		atmo[0],
		atmo[1],
		epheflag,
	)

	rsmi = (
		swe.CALC_SET
		| swe.BIT_DISC_CENTER
		| swe.BIT_NO_REFRACTION
	)
	isSetMissing, tSet = swe.rise_trans(
		tjd,
		pl,
		rsmi,
		geopos,
		atmo[0],
		atmo[1],
		epheflag,
	)

	return {
		'sunrise': None
		if isRiseMissing
		else parseSweTime(tRise),
		'sunset': None
		if isSetMissing
		else parseSweTime(tSet),
	}
