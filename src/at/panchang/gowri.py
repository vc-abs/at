from at.core.constants import (
	weekdays,
	gowri_segment_name_cycle,
	gowri_segment_meanings,
	gowri_segment_scores,
	gowri_rahu_segment_by_vaara,
	gowri_night_weekday_offset,
	gowri_segment_count,
)



def insert_visham(values, segment_index):
	insert_at = segment_index - 1
	return values[:insert_at] + ['visham'] + values[insert_at:]



def get_segment_duration(start, end):
	return (end - start) / gowri_segment_count



def get_segment_bounds(start, end, segment_index):
	segment_duration = get_segment_duration(
		start,
		end,
	)
	segment_start = start + (
		segment_duration * (segment_index - 1)
	)
	segment_end = start + (
		segment_duration * segment_index
	)
	return segment_start, segment_end



def get_segment_index(event_time, start, end):
	if not start <= event_time < end:
		return None

	segment_duration = get_segment_duration(
		start,
		end,
	)
	elapsed = event_time - start
	return int(elapsed / segment_duration) + 1



def get_effective_weekday(vaara, tod):
	if tod == 'day':
		return vaara

	weekday_index = weekdays.index(vaara)
	return weekdays[
		(weekday_index + gowri_night_weekday_offset)
		% len(weekdays)
	]



def get_schedule_names(vaara, tod):
	effective_weekday = get_effective_weekday(
		vaara,
		tod,
	)
	base_index = weekdays.index(
		effective_weekday
	)
	base_sequence = [
		gowri_segment_name_cycle[
			(base_index + offset)
			% len(gowri_segment_name_cycle)
		]
		for offset in range(
			len(gowri_segment_name_cycle)
		)
	]
	return insert_visham(
		base_sequence,
		gowri_rahu_segment_by_vaara[
			effective_weekday
		],
	)



def get_gowri_segment_by_index(
	panchang, segment_index, tod
):
	rise_and_set = panchang.rise_and_set
	period_start = (
		rise_and_set['sunrise']
		if tod == 'day'
		else rise_and_set['sunset']
	)
	period_end = (
		rise_and_set['sunset']
		if tod == 'day'
		else rise_and_set['nextRise']
	)
	name = get_schedule_names(
		panchang.vaara,
		tod,
	)[segment_index - 1]
	segment_start, segment_end = get_segment_bounds(
		period_start,
		period_end,
		segment_index,
	)

	return {
		'segment': segment_index,
		'tod': tod,
		'name': name,
		'meaning': gowri_segment_meanings[name],
		'score': gowri_segment_scores[name],
		'startsAt': segment_start,
		'endsAt': segment_end,
	}



def get_gowri_schedule(panchang):
	return {
		'day': [
			get_gowri_segment_by_index(
				panchang,
				segment_index,
				'day',
			)
			for segment_index in range(
				1,
				gowri_segment_count + 1,
			)
		],
		'night': [
			get_gowri_segment_by_index(
				panchang,
				segment_index,
				'night',
			)
			for segment_index in range(
				1,
				gowri_segment_count + 1,
			)
		],
	}



def get_current_gowri_segment(panchang):
	event_time = panchang._chart.config['datetime']
	rise_and_set = panchang.rise_and_set
	tod = panchang.tod
	period_start = (
		rise_and_set['sunrise']
		if tod == 'day'
		else rise_and_set['sunset']
	)
	period_end = (
		rise_and_set['sunset']
		if tod == 'day'
		else rise_and_set['nextRise']
	)
	segment_index = get_segment_index(
		event_time,
		period_start,
		period_end,
	)
	segment_index = segment_index or gowri_segment_count
	return get_gowri_segment_by_index(
		panchang,
		segment_index,
		tod,
	)



def get_gowri_window_flags(panchang):
	segment = get_current_gowri_segment(panchang)
	return {
		'gowri': segment['name'],
		'gowriScore': segment['score'],
		'gowriM': segment['meaning'],
		'gowriS': segment['segment'],
		'gowriT': segment['tod'],
		'gowriStart': segment['startsAt'],
		'gowriEnd': segment['endsAt'],
		'gowriF': '|'.join(
			sorted(
				{
					segment['name'],
					segment['tod'],
				}
			)
			)
		}


__all__ = [
	get_gowri_schedule,
	get_current_gowri_segment,
	get_gowri_window_flags,
	get_schedule_names,
]
