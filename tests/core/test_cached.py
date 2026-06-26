import pytest

from at.core.cached import Cached


class _demo_cached(Cached):
	def __init__(self):
		super().__init__()
		self.calls = 0

	def _get_value(self):
		self.calls += 1
		return 42


class _missing_getter(Cached):
	pass


def test_cached_getattr_computes_once_and_reuses_value():
	obj = _demo_cached()

	assert obj.value == 42
	assert obj.value == 42
	assert obj.calls == 1


def test_cached_getattr_raises_for_missing_getter():
	obj = _missing_getter()
	with pytest.raises(AttributeError):
		_ = obj.anything
