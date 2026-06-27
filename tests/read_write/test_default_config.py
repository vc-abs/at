from at.read_write.get_default_config import get_default_config


def test_get_default_config_shape_and_defaults():
	cfg = get_default_config()

	for key in [
		'year',
		'month',
		'day',
		'hour',
		'minute',
		'second',
	]:
		assert key in cfg
