import swisseph as swe

signCount = 12
signs = [
	i + 1 for i in range(0, signCount)
]
degrees = 360
maxPossibleDistance = degrees / 2
daysPerYear = 365.256364
houseCount = signCount
signWidth = degrees / signCount
tithiCount = 30
tithis = range(0, tithiCount)
pakshaTithiCount = tithiCount / 2
houses = [
	i + 1 for i in range(0, houseCount)
]
horasPerDay = 24
weekdays = [
	'sunday',
	'monday',
	'tuesday',
	'wednesday',
	'thursday',
	'friday',
	'saturday',
]
daysInAWeek = len(weekdays)
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

dayRulers = [
	'sun',
	'moon',
	'mars',
	'mercury',
	'jupiter',
	'venus',
	'saturn',
]
weekdayLords = {
	k: v
	for k, v in zip(weekdays, dayRulers)
}
horaLordSequence = [
	'sun',
	'venus',
	'mercury',
	'moon',
	'saturn',
	'jupiter',
	'mars',
]

objectProps = {
	'sun': {
		'exaltation': 10,
		'debilitation': 190,
		'ojaYugmaBala': [15, 0],
		'aspects': [7],
		'quality': 'malefic',
		'gender': 'male',
		'digBalaHouse': 10,
		'moolaTrikona': [120, 140],
		'tod': 'day',
		'weekday': 'sunday',
		'ayana': 'north',
		'position': 'anchor',
		'meanSpeed': 0.9856,  # degrees per day
		'sweID': swe.SUN,
	},
	'moon': {
		'exaltation': 33,
		'debilitation': 213,
		'ojaYugmaBala': [0, 15],
		'aspects': [7],
		'quality': 'conditional',
		'gender': 'female',
		'digBalaHouse': 4,
		'moolaTrikona': [33, 60],
		'tod': 'night',
		'weekday': 'monday',
		'ayana': 'south',
		'position': 'satellite',
		'meanSpeed': 13.1764,
		'sweID': swe.MOON,
	},
	'mars': {
		'exaltation': 298,
		'debilitation': 118,
		'ojaYugmaBala': [15, 0],
		'aspects': [4, 7, 8],
		'quality': 'malefic',
		'gender': 'male',
		'digBalaHouse': 10,
		'moolaTrikona': [0, 12],
		'tod': 'night',
		'weekday': 'tuesday',
		'ayana': 'north',
		'position': 'outer',
		'meanSpeed': 0.5240,
		'sweID': swe.MARS,
	},
	'mercury': {
		'exaltation': 165,
		'debilitation': 345,
		'ojaYugmaBala': [15, 0],
		'aspects': [7],
		'quality': 'conditional',
		'gender': 'neutral',
		'digBalaHouse': 1,
		'moolaTrikona': [165, 170],
		'tod': 'both',
		'weekday': 'wednesday',
		'ayana': 'both',
		'position': 'inner',
		'meanSpeed': 1.3833,
		'sweID': swe.MERCURY,
	},
	'jupiter': {
		'exaltation': 95,
		'debilitation': 275,
		'ojaYugmaBala': [15, 0],
		'aspects': [7],
		'quality': 'benefic',
		'gender': 'male',
		'digBalaHouse': 1,
		'moolaTrikona': [240, 250],
		'tod': 'day',
		'weekday': 'thursday',
		'ayana': 'north',
		'position': 'outer',
		'meanSpeed': 0.0831,
		'sweID': swe.JUPITER,
	},
	'venus': {
		'exaltation': 357,
		'debilitation': 177,
		'ojaYugmaBala': [0, 15],
		'aspects': [5, 7, 9],
		'quality': 'benefic',
		'gender': 'female',
		'digBalaHouse': 4,
		'moolaTrikona': [180, 195],
		'tod': 'day',
		'weekday': 'friday',
		'position': 'inner',
		'ayana': 'north',
		'meanSpeed': 1.2,
		'sweID': swe.VENUS,
	},
	'saturn': {
		'exaltation': 200,
		'debilitation': 20,
		'ojaYugmaBala': [15, 0],
		'aspects': [3, 7, 10],
		'quality': 'malefic',
		'gender': 'neutral',
		'digBalaHouse': 7,
		'moolaTrikona': [300, 320],
		'tod': 'night',
		'weekday': 'saturday',
		'ayana': 'south',
		'position': 'outer',
		'meanSpeed': 0.0335,
		'sweID': swe.SATURN,
	},
	'rahu': {
		'quality': 'malefic',
		'sweID': swe.MEAN_NODE,
	},
	'ketu': {
		'quality': 'malefic',
	},
}
objectIDs = {
	object: objectAttrs['sweID']
	for object, objectAttrs in objectProps.items()
	if 'sweID' in objectAttrs
}
houseQualities = [
	'kendra',
	'panapara',
	'apoklima',
]

kendradiBala = {
	'kendra': 60,
	'panapara': 30,
	'apoklima': 15,
}

signLords = [
	None,
	'mars',
	'venus',
	'mercury',
	'moon',
	'sun',
	'mercury',
	'venus',
	'mars',
	'jupiter',
	'saturn',
	'saturn',
	'jupiter',
]

planetaryFriendships = {
	('sun', 'sun'): 2,
	('sun', 'moon'): 1,
	('sun', 'mars'): 1,
	('sun', 'jupiter'): 1,
	('sun', 'mercury'): 0,
	('sun', 'venus'): -1,
	('sun', 'saturn'): -1,
	('sun', 'rahu'): -1,
	('sun', 'ketu'): -1,
	('moon', 'moon'): 2,
	('moon', 'sun'): 1,
	('moon', 'mercury'): 1,
	('moon', 'mars'): 0,
	('moon', 'jupiter'): 0,
	('moon', 'venus'): 0,
	('moon', 'saturn'): 0,
	('moon', 'rahu'): 0,
	('moon', 'ketu'): 0,
	('mars', 'mars'): 2,
	('mars', 'sun'): 1,
	('mars', 'moon'): 1,
	('mars', 'jupiter'): 1,
	('mars', 'venus'): 0,
	('mars', 'saturn'): 0,
	('mars', 'mercury'): -1,
	('mars', 'rahu'): -1,
	('mars', 'ketu'): -1,
	('mercury', 'mercury'): 2,
	('mercury', 'sun'): 1,
	('mercury', 'venus'): 1,
	('mercury', 'mars'): 0,
	('mercury', 'jupiter'): 0,
	('mercury', 'saturn'): 0,
	('mercury', 'moon'): -1,
	('mercury', 'rahu'): 0,
	('mercury', 'ketu'): 0,
	('jupiter', 'jupiter'): 2,
	('jupiter', 'sun'): 1,
	('jupiter', 'moon'): 1,
	('jupiter', 'mars'): 1,
	('jupiter', 'saturn'): 0,
	('jupiter', 'mercury'): -1,
	('jupiter', 'venus'): -1,
	('jupiter', 'rahu'): -1,
	('jupiter', 'ketu'): -1,
	('venus', 'venus'): 2,
	('venus', 'mercury'): 1,
	('venus', 'saturn'): 1,
	('venus', 'mars'): 0,
	('venus', 'jupiter'): 0,
	('venus', 'sun'): -1,
	('venus', 'moon'): -1,
	('venus', 'rahu'): 0,
	('venus', 'ketu'): 0,
	('saturn', 'saturn'): 2,
	('saturn', 'mercury'): 1,
	('saturn', 'venus'): 1,
	('saturn', 'jupiter'): 0,
	('saturn', 'sun'): -1,
	('saturn', 'moon'): -1,
	('saturn', 'mars'): -1,
	('saturn', 'rahu'): 0,
	('saturn', 'ketu'): 0,
	('rahu', 'rahu'): 2,
	('rahu', 'sun'): -1,
	('rahu', 'moon'): 0,
	('rahu', 'mars'): -1,
	('rahu', 'mercury'): 0,
	('rahu', 'jupiter'): -1,
	('rahu', 'venus'): 0,
	('rahu', 'saturn'): 0,
	('rahu', 'ketu'): -1,
	('ketu', 'ketu'): 2,
	('ketu', 'sun'): -1,
	('ketu', 'moon'): 0,
	('ketu', 'mars'): -1,
	('ketu', 'mercury'): 0,
	('ketu', 'jupiter'): -1,
	('ketu', 'venus'): 0,
	('ketu', 'saturn'): 0,
	('ketu', 'rahu'): -1,
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

ayanamsaSWEConstants = {
	'fagan_bradley': swe.SIDM_FAGAN_BRADLEY,
	'lahiri': swe.SIDM_LAHIRI,
	'deluce': swe.SIDM_DELUCE,
	'raman': swe.SIDM_RAMAN,
	'ushashashi': swe.SIDM_USHASHASHI,
	'krishnamurti': swe.SIDM_KRISHNAMURTI,
	'djwhal_khul': swe.SIDM_DJWHAL_KHUL,
	'yukteshwar': swe.SIDM_YUKTESHWAR,
	'jn_bhasin': swe.SIDM_JN_BHASIN,
	'aldebaran_15tau': swe.SIDM_ALDEBARAN_15TAU,
	'hipparchos': swe.SIDM_HIPPARCHOS,
	'sassanian': swe.SIDM_SASSANIAN,
	'galcent_0sag': swe.SIDM_GALCENT_0SAG,
	'j2000': swe.SIDM_J2000,
	'j1900': swe.SIDM_J1900,
	'b1950': swe.SIDM_B1950,
	'suryasiddhanta': swe.SIDM_SURYASIDDHANTA,
	'suryasiddhanta_msun': swe.SIDM_SURYASIDDHANTA_MSUN,
	'aryabhata': swe.SIDM_ARYABHATA,
	'aryabhata_msun': swe.SIDM_ARYABHATA_MSUN,
	'ss_citra': swe.SIDM_SS_CITRA,
	'ss_revati': swe.SIDM_SS_REVATI,
	'true_revati': swe.SIDM_TRUE_REVATI,
	'true_pushya': swe.SIDM_TRUE_PUSHYA,
	'galcent_rgilbrand': swe.SIDM_GALCENT_RGILBRAND,
	'galequ_iau1958': swe.SIDM_GALEQU_IAU1958,
	'galequ_true': swe.SIDM_GALEQU_TRUE,
	'user': swe.SIDM_USER,
}
