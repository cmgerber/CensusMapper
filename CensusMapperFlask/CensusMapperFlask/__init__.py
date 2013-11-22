import flask

app = flask.Flask('CensusMapperFlask')

import CensusMapperFlask.views
import CensusMapperFlask.insert_user
import CensusMapperFlask.login_logout
