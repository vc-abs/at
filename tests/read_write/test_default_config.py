from at.read_write.get_default_config import (
	get_default_config,
	select_all_query,
)


def test_get_default_config_shape_and_defaults():
	cfg = get_default_config()

	assert cfg['query'] == select_all_query
	assert cfg['constants'] == {}
	assert cfg['fieldSets'] == {}
	assert cfg['customColumns'] == {}
	assert cfg['skipColumns'] == []
	assert cfg['order'] == {}

	for key in [
		'year',
		'month',
		'day',
		'hour',
		'minute',
		'second',
	]:
		assert key in cfg
