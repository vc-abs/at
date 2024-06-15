from core.Cached import Cached

nakshatraLords = [
	'ketu',
	'venus',
	'sun',
	'moon',
	'mars',
	'rahu',
	'jupiter',
	'saturn',
	'mercury',
]
nakshatraLordCount = len(nakshatraLords)


class Dasha(Cached):
	def __init__(self, chart):
		super().__init__()
		self._chart = chart

	def _getNakshatraLord(self):
		nakshatraLordIndex = (
			self._chart.panchang.nakshatraNumber
			- 1
		) % nakshatraLordCount

		return {
			'nakshatraLord': nakshatraLords[
				nakshatraLordIndex
			],
		}
