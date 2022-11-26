import re
import string

from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from settings import Config

app = Flask(__name__, template_folder='../html', static_folder='../html')
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
SHORT_URL_SIZE_MAX = 16
SHORT_URL_SIZE_MIN = LONG_URL_SIZE_MIN = 0
SHORT_URL_SIZE_GENERATE = 6
LONG_URL_SIZE_MAX = 128
SHORT_URL_SYMBOLS = string.ascii_letters + string.digits
GET_SHORT_ID_TRIALS = 5
localhost = 'http://localhost/'
short_url_regex = f"^[{re.escape(SHORT_URL_SYMBOLS)}]+$"

from . import views, models, error_handlers, api_views
