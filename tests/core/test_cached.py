import pytest

from at.core.Cached import Cached


class _DemoCached(Cached):
	def __init__(self):
		super().__init__()
		self.calls = 0

	def _getValue(self):
		self.calls += 1
		return 42


class _MissingGetter(Cached):
	pass


def test_cached_getattr_computes_once_and_reuses_value():
	obj = _DemoCached()

	assert obj.value == 42
	assert obj.value == 42
	assert obj.calls == 1


def test_cached_getattr_raises_for_missing_getter():
	obj = _MissingGetter()
	with pytest.raises(AttributeError):
		_ = obj.anything
