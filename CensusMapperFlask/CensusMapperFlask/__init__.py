import flask
app = flask.Flask(__name__)

import CensusMapperFlask.views
import CensusMapperFlask.db_insert_user
import CensusMapperFlask.db_models