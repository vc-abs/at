signCount = 12
signs = [
	i + 1 for i in range(0, signCount)
]
degrees = 360
daysPerYear = 365.256364
houseCount = signCount
signWidth = degrees / signCount
tithiCount = 30
tithis = range(0, tithiCount)
pakshaTithiCount = tithiCount / 2
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

exaltationDegrees = {
	'sun': 10,
	'moon': 33,
	'mars': 298,
	'mercury': 165,
	'jupiter': 95,
	'venus': 357,
	'saturn': 200,
}

debilitationDegrees = {
	'sun': 190,
	'moon': 213,
	'mars': 118,
	'mercury': 345,
	'jupiter': 275,
	'venus': 177,
	'saturn': 20,
}


# #TODO: Create a CSV with other properties of nakshatras for better analysis.
nakshatras = [
	'asvini',
	'bharani',
	'krittika',
	'rohini',
	'mrigashira',
	'ardra',
	'punarvasu',
	'pushya',
	'ashlesha',
	'magha',
	'purvaPhalguni',
	'uttaraPhalguni',
	'hasta',
	'chitra',
	'svati',
	'vishakha',
	'anuradha',
	'jyeshta',
	'mula',
	'purvaAshadha',
	'uttaraAshadha',
	'shravana',
	'dhanishta',
	'shatabhisha',
	'purvaBhadrapada',
	'uttaraBhadrapada',
	'revati',
]

nakshatraCount = len(nakshatras)
nakshatraWidth = (
	degrees / nakshatraCount
)
padasPerNakshatra = 4
padaCount = (
	nakshatraCount * padasPerNakshatra
)
