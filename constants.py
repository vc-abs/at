signCount = 12
signs = [
	i + 1 for i in range(0, signCount)
]
houseCount = signCount
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
