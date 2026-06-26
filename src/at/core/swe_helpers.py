from datetime import (
	datetime,
	timezone,
	timedelta,
)
import swisseph as swe
from at.core.constants import (
	object_props,
	degrees,
	ayanamsa_swe_constants,
)

minutes_per_hor = 60
seconds_per_hour = 3600
seconds_per_minute = 60
floating_point_precision_correction_seconds = 0.001

rise_flags = (
	swe.CALC_RISE | swe.BIT_HINDU_RISING
)
set_flags = (
	swe.CALC_SET | swe.BIT_HINDU_RISING
)

gregflag = swe.GREG_CAL
# pressure & temperature or irrelevant for hindu method, can be set to 0
atmo = (1013.25, 15)
altitude = 0.0
SUN = swe.SUN

utc_time_zone = timezone(
	offset=timedelta(
		hours=0,
		minutes=0,
	)
)


def get_rounded_seconds(float_hours):
	return int(
		float_hours * seconds_per_hour
		+ floating_point_precision_correction_seconds
	)


def float_to_hms(float_hours):
	total_seconds = get_rounded_seconds(
		float_hours
	)
	hours, rem_seconds = divmod(
		total_seconds,
		seconds_per_hour,
	)
	minutes, seconds = divmod(
		rem_seconds,
		seconds_per_minute,
	)

	return hours, minutes, seconds


def jdt_to_date_time(
	from_tret, from_tz_info=utc_time_zone
):
	year, month, day, float_hour = (
		swe.revjul(from_tret, gregflag)
	)

	return (
		datetime(
			year,
			month,
			day,
			tzinfo=utc_time_zone,
		)
		+ timedelta(
			seconds=get_rounded_seconds(
				float_hour
			)
		)
	).astimezone(from_tz_info)


def date_time_to_jdt(from_value):
	offset_seconds = (
		from_value.utcoffset()
		or datetime.now(
			utc_time_zone
		).utcoffset()
	).seconds
	return swe.julday(
		from_value.year,
		from_value.month,
		from_value.day,
		from_value.hour
		+ (
			(
				from_value.minute
				* seconds_per_minute
				+ from_value.second
				- offset_seconds
				+ floating_point_precision_correction_seconds
			)
			/ seconds_per_hour
		),
	)


# #Note: Precision of JDT is more than that of eventTime configuration, which is at the second level. This creates issues in computing rise and set times and is fixed by neglecting tiny differences.
def is_jdt_greater(base_jdt, compared_jdt):
	is_difference_tiny = (
		abs(base_jdt - compared_jdt) < 0.00001
	)

	return (
		False
		if is_difference_tiny
		else base_jdt > compared_jdt
	)


def get_next_rise(tjd, geopos):
	is_rise_missing, t_rise = swe.rise_trans(
		tjd,
		SUN,
		rise_flags,
		geopos,
		atmo[0],
		atmo[1],
	)

	return (
		None if is_rise_missing else t_rise[0]
	)


# #NOTE: There's some one minute difference in both sunrise and sunset times, when compared to JH. The flags used are to get closer to those values, and are not from proper understanding.
# #FROM: https://astrorigin.com/pyswisseph/sphinx/programmers_manual/planetary_phenomena/risings_settings_meridian_transits.html?highlight=bit_hindu_rising
def get_rise_and_set_times(config):
	event_time, latitude, longitude = (
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
		event_time.year,
		event_time.month,
		event_time.day,
		0,
		gregflag,
	)
	event_time_julian = date_time_to_jdt(
		event_time
	)
	tjd = tjd - (longitude / 360.0)
	t_this_rise = get_next_rise(tjd, geopos)
	direction = t_this_rise and (
		-1
		if is_jdt_greater(
			t_this_rise, event_time_julian
		)
		else 1
	)
	offset = (
		1.999 if direction < 0 else 0.001
	) * direction

	t_other_rise = (
		None
		if t_this_rise is None
		else get_next_rise(
			t_this_rise + offset,
			geopos,
		)
	)

	t_rise = (
		t_this_rise
		if direction > 0
		else t_other_rise
	)
	t_next_rise = (
		t_other_rise
		if direction > 0
		else t_this_rise
	)

	is_set_missing, t_set = swe.rise_trans(
		t_rise,
		SUN,
		set_flags,
		geopos,
		atmo[0],
		atmo[1],
	)

	return {
		'sunrise': None
		if t_rise is None
		else jdt_to_date_time(
			t_rise, event_time.tzinfo
		),
		'sunset': None
		if is_set_missing
		else jdt_to_date_time(
			t_set[0], event_time.tzinfo
		),
		'nextRise': None
		if not t_next_rise
		else jdt_to_date_time(
			t_next_rise, event_time.tzinfo
		),
	}


def set_ayanamsa(ayanamsa):
	swe.set_sid_mode(
		ayanamsa_swe_constants[ayanamsa],
		0,
		0,
	)


def get_ayanamsa_offset(event_time):
	event_time_jd = date_time_to_jdt(event_time)

	return swe.get_ayanamsa_ex(
		event_time_jd, 0
	)[1]


def unset_ayanamsa():
	swe.close()


# #NOTE: This function is not actively used, but was kept as it seems useful and it incurred quite a chunk of effort.
def get_solar_crossing_time(
	longitude, start_date
):
	jd_start_date = date_time_to_jdt(start_date)

	jd_cross = swe.solcross(
		longitude,
		jd_start_date,
		swe.FLG_SIDEREAL
		| swe.FLG_CENTER_BODY,
	)
	return jdt_to_date_time(
		jd_cross,
		start_date.tzinfo or utc_time_zone,
	)


def get_planet_position(
	planet, event_time
):
	return swe.calc_ut(
		event_time,
		object_props[planet]['sweID'],
		swe.FLG_SIDEREAL,
	)[0][0]


def get_planet_mean_longitude_and_difference(
	planet,
	event_time,
	avg_sample_days=365000,
):
	planet_props = object_props[planet]
	planet_mean_speed = planet_props[
		'meanSpeed'
	]
	event_time = date_time_to_jdt(event_time)
	sample_start_time = (
		event_time - avg_sample_days
	)

	event_longitude = get_planet_position(
		planet, event_time
	)
	sample_start_longitude = (
		get_planet_position(
			planet, sample_start_time
		)
	)
	mean_longitude = (
		sample_start_longitude
		+ planet_mean_speed
		* (event_time - sample_start_time)
	) % degrees
	difference = (
		event_longitude - mean_longitude
	)

	return (
		mean_longitude,
		difference,
	)
