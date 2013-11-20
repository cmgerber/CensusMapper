import flask

app = flask.Flask('CensusMapperFlask')

import CensusMapperFlask.views
import CensusMapperFlask.db_insert_user
import CensusMapperFlask.db_login_logout
