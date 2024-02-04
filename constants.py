signCount = 12
signs = [
	i + 1 for i in range(0, signCount)
]
degrees = 360
houseCount = signCount
signWidth = degrees / signCount
tithiCount = 30
tithis = range(0, tithiCount)
houses = [
	i + 1 for i in range(0, houseCount)
]
weekDays = [
	'sunday',
	'monday',
	'tuesday',
	'wednesday',
	'thursday',
	'friday',
	'saturday',
]
daysInAWeek = len(weekDays)
planets = [
	'sun',
	'moon',
	'mars',
	'mercury',
	'jupiter',
	'venus',
	'saturn',
]

nodes = [
	'ketu',
	'rahu',
]

angles = ['asc']

ashtaka = angles + planets

objects = ashtaka + nodes
