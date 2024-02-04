from core.Cached import Cached


class Panchang(Cached):
	def __init__(self, chart):
		super().__init__()
		self._chart = chart
