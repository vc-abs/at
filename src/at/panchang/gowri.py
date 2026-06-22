from at.core.constants import (
	weekdays,
	gowriSegmentNameCycle,
	gowriSegmentMeanings,
	gowriSegmentScores,
	gowriRahuSegmentByVaara,
	gowriNightWeekdayOffset,
	gowriSegmentCount,
)



def insertVisham(values, segmentIndex):
	insertAt = segmentIndex - 1
	return values[:insertAt] + ['visham'] + values[insertAt:]



def getSegmentDuration(start, end):
	return (end - start) / gowriSegmentCount



def getSegmentBounds(start, end, segmentIndex):
	segmentDuration = getSegmentDuration(
		start,
		end,
	)
	segmentStart = start + (
		segmentDuration * (segmentIndex - 1)
	)
	segmentEnd = start + (
		segmentDuration * segmentIndex
	)
	return segmentStart, segmentEnd



def getSegmentIndex(eventTime, start, end):
	if not start <= eventTime < end:
		return None

	segmentDuration = getSegmentDuration(
		start,
		end,
	)
	elapsed = eventTime - start
	return int(elapsed / segmentDuration) + 1



def getEffectiveWeekday(vaara, tod):
	if tod == 'day':
		return vaara

	weekdayIndex = weekdays.index(vaara)
	return weekdays[
		(weekdayIndex + gowriNightWeekdayOffset)
		% len(weekdays)
	]



def getScheduleNames(vaara, tod):
	effectiveWeekday = getEffectiveWeekday(
		vaara,
		tod,
	)
	baseIndex = weekdays.index(
		effectiveWeekday
	)
	baseSequence = [
		gowriSegmentNameCycle[
			(baseIndex + offset)
			% len(gowriSegmentNameCycle)
		]
		for offset in range(
			len(gowriSegmentNameCycle)
		)
	]
	return insertVisham(
		baseSequence,
		gowriRahuSegmentByVaara[
			effectiveWeekday
		],
	)



def getGowriSegmentByIndex(
	panchang, segmentIndex, tod
):
	riseAndSet = panchang.riseAndSet
	periodStart = (
		riseAndSet['sunrise']
		if tod == 'day'
		else riseAndSet['sunset']
	)
	periodEnd = (
		riseAndSet['sunset']
		if tod == 'day'
		else riseAndSet['nextRise']
	)
	name = getScheduleNames(
		panchang.vaara,
		tod,
	)[segmentIndex - 1]
	segmentStart, segmentEnd = getSegmentBounds(
		periodStart,
		periodEnd,
		segmentIndex,
	)

	return {
		'segment': segmentIndex,
		'tod': tod,
		'name': name,
		'meaning': gowriSegmentMeanings[name],
		'score': gowriSegmentScores[name],
		'startsAt': segmentStart,
		'endsAt': segmentEnd,
	}



def getGowriSchedule(panchang):
	return {
		'day': [
			getGowriSegmentByIndex(
				panchang,
				segmentIndex,
				'day',
			)
			for segmentIndex in range(
				1,
				gowriSegmentCount + 1,
			)
		],
		'night': [
			getGowriSegmentByIndex(
				panchang,
				segmentIndex,
				'night',
			)
			for segmentIndex in range(
				1,
				gowriSegmentCount + 1,
			)
		],
	}



def getCurrentGowriSegment(panchang):
	eventTime = panchang._chart.config['datetime']
	riseAndSet = panchang.riseAndSet
	tod = panchang.tod
	periodStart = (
		riseAndSet['sunrise']
		if tod == 'day'
		else riseAndSet['sunset']
	)
	periodEnd = (
		riseAndSet['sunset']
		if tod == 'day'
		else riseAndSet['nextRise']
	)
	segmentIndex = getSegmentIndex(
		eventTime,
		periodStart,
		periodEnd,
	)
	segmentIndex = segmentIndex or gowriSegmentCount
	return getGowriSegmentByIndex(
		panchang,
		segmentIndex,
		tod,
	)



def getGowriWindowFlags(panchang):
	segment = getCurrentGowriSegment(panchang)
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
	getGowriSchedule,
	getCurrentGowriSegment,
	getGowriWindowFlags,
	getScheduleNames,
]
