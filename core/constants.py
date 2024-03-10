signCount = 12
signs = [
	i + 1 for i in range(0, signCount)
]
degrees = 360
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
padasPerNakshatra = 4
padaCount = (
	nakshatraCount * padasPerNakshatra
)
