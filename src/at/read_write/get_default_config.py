from datetime import (
	datetime,
)

select_all_query = 'ilevel_0 in ilevel_0'

select_all_selection = select_all_query
select_all_field_sets = {
	'scenario': 'all',
	'panchang': 'all',
}


def get_default_config():
	now = datetime.now()

	return {
		'year': now.year,
		'month': now.month,
		'day': now.day,
		'hour': now.hour,
		'minute': now.minute,
		'second': now.second,
		'baseConfigurations': {},
	}
