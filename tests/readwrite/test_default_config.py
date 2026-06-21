from at.readWrite.getDefaultConfig import (
	getDefaultConfig,
	selectAllQuery,
)


def test_get_default_config_shape_and_defaults():
	cfg = getDefaultConfig()

	assert cfg['query'] == selectAllQuery
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
