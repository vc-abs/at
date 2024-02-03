signCount = 12
signs = [
	i + 1 for i in range(0, signCount)
]
degrees = 360
houseCount = signCount
signWidth = degrees / signCount
tithiCount = 30
houses = [
	i + 1 for i in range(0, houseCount)
]

planets = [
	'moon',
	'sun',
	'mercury',
	'venus',
	'mars',
	'jupiter',
	'saturn',
]

nodes = [
	'ketu',
	'rahu',
]

angles = ['asc']

ashtaka = angles + planets

objects = ashtaka + nodes
