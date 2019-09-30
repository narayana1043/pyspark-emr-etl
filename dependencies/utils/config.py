import getpass


def detect_env():
	user = getpass.getuser()
	if user in ['hadoop', 'ubuntu']:
		return 'prod'
	else:
		return 'local'


def get_config():
	config = {
		"local": {
			"DB_NAME": {
				"host": "localhost",
				"user": "username",
				"passwd": "password",
				"db": "db_name",
				"port": "3306"
			},
			"ES_HOST": "http://xx.xx.xx.xx:9200/",
			"JANUS_HOST": "xx.xx.xx.xx"
		},
		"prod": {
			"ana_prod_v1": {
				"host": "remotehost",
				"user": "username",
				"passwd": "password",
				"db": "db_name",
				"port": "3306"
			},
			"ES_HOST": "http://xx.xx.xx.xx:9200/",
			"JANUS_HOST": "xx.xx.xx.xx"
		},
	}
	status = detect_env()
	config = config[status]
	config['status'] = status
	return config
