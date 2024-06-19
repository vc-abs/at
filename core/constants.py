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

objectProps = {
	'sun': {
		'exaltation': 10,
		'debilitation': 190,
		'ojaYugmaBala': [15, 0],
		'quality': 'malefic',
	},
	'moon': {
		'exaltation': 33,
		'debilitation': 213,
		'ojaYugmaBala': [0, 15],
		# #TODO: Implement ways to find planetary quality for Moon and Mercury.
		'quality': 'conditional',
	},
	'mars': {
		'exaltation': 298,
		'debilitation': 118,
		'ojaYugmaBala': [15, 0],
		'quality': 'malefic',
	},
	'mercury': {
		'exaltation': 165,
		'debilitation': 345,
		# #TODO: Looks like Mercury and Saturn is assigned zeroes like other planets in some systems, get better understanding here.
		'ojaYugmaBala': [7.5, 15],
		'quality': 'conditional',
	},
	'jupiter': {
		'exaltation': 95,
		'debilitation': 275,
		'ojaYugmaBala': [15, 0],
		'quality': 'benefic',
	},
	'venus': {
		'exaltation': 357,
		'debilitation': 177,
		'ojaYugmaBala': [0, 15],
		'quality': 'benefic',
	},
	'saturn': {
		'exaltation': 200,
		'debilitation': 20,
		'ojaYugmaBala': [15, 7.5],
		'quality': 'malefic',
	},
	'rahu': {
		'quality': 'malefic',
	},
	'ketu': {
		'quality': 'malefic',
	},
}

houseQualities = [
	'kendra',
	'panapara',
	'apoklima',
]

kendradiBala = {
	'kendra': {
		'benefic': 60,
		'malefic': 30,
		'conditional': 45,
	},
	'panapara': {
		'benefic': 30,
		'malefic': 60,
		'conditional': 45,
	},
	'apoklima': {
		'benefic': 15,
		'malefic': 15,
		'conditional': 15,
	},
}

signLords = [
	None,
	'mars',
	'venus',
	'mercury',
	'sun',
	'moon',
	'venus',
	'mercury',
	'mars',
	'jupiter',
	'saturn',
	'saturn',
	'jupiter',
]

planetaryFriendships = {
	('sun', 'moon'): 1,
	('sun', 'mars'): 1,
	('sun', 'jupiter'): 1,
	('sun', 'mercury'): 0,
	('sun', 'venus'): -1,
	('sun', 'saturn'): -1,
	('sun', 'rahu'): -1,
	('sun', 'ketu'): -1,
	('moon', 'sun'): 1,
	('moon', 'mercury'): 1,
	('moon', 'mars'): 0,
	('moon', 'jupiter'): 0,
	('moon', 'venus'): 0,
	('moon', 'saturn'): 0,
	('moon', 'rahu'): 0,
	('moon', 'ketu'): 0,
	('mars', 'sun'): 1,
	('mars', 'moon'): 1,
	('mars', 'jupiter'): 1,
	('mars', 'venus'): 0,
	('mars', 'saturn'): 0,
	('mars', 'mercury'): -1,
	('mars', 'rahu'): -1,
	('mars', 'ketu'): -1,
	('mercury', 'sun'): 1,
	('mercury', 'venus'): 1,
	('mercury', 'mars'): 0,
	('mercury', 'jupiter'): 0,
	('mercury', 'saturn'): 0,
	('mercury', 'moon'): -1,
	('mercury', 'rahu'): 0,
	('mercury', 'ketu'): 0,
	('jupiter', 'sun'): 1,
	('jupiter', 'moon'): 1,
	('jupiter', 'mars'): 1,
	('jupiter', 'saturn'): 0,
	('jupiter', 'mercury'): -1,
	('jupiter', 'venus'): -1,
	('jupiter', 'rahu'): -1,
	('jupiter', 'ketu'): -1,
	('venus', 'mercury'): 1,
	('venus', 'saturn'): 1,
	('venus', 'mars'): 0,
	('venus', 'jupiter'): 0,
	('venus', 'sun'): -1,
	('venus', 'moon'): -1,
	('venus', 'rahu'): 0,
	('venus', 'ketu'): 0,
	('saturn', 'mercury'): 1,
	('saturn', 'venus'): 1,
	('saturn', 'jupiter'): 0,
	('saturn', 'sun'): -1,
	('saturn', 'moon'): -1,
	('saturn', 'mars'): -1,
	('saturn', 'rahu'): 0,
	('saturn', 'ketu'): 0,
	('rahu', 'sun'): -1,
	('rahu', 'moon'): 0,
	('rahu', 'mars'): -1,
	('rahu', 'mercury'): 0,
	('rahu', 'jupiter'): -1,
	('rahu', 'venus'): 0,
	('rahu', 'saturn'): 0,
	('rahu', 'ketu'): -1,
	('ketu', 'sun'): -1,
	('ketu', 'moon'): 0,
	('ketu', 'mars'): -1,
	('ketu', 'mercury'): 0,
	('ketu', 'jupiter'): -1,
	('ketu', 'venus'): 0,
	('ketu', 'saturn'): 0,
	('ketu', 'rahu'): -1,
}

# #FROM: The book Vedic Astrology - An Integrated Approach by P. V. R. Narasimmha Rao.
moolaTrikonaPositions = {
	'sun': {'start': 120, 'end': 140},
	'moon': {'start': 33, 'end': 60},
	'mars': {'start': 0, 'end': 12},
	'mercury': {'start': 165, 'end': 170},
	'jupiter': {'start': 240, 'end': 250},
	'venus': {'start': 180, 'end': 195},
	'saturn': {'start': 300, 'end': 320},
}

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
