
from flask import Flask
from flask_sqlalchemy import SQLAlchemy


# needed by beanstalk
application = Flask(__name__)
application.config.from_object('config')
# config
#application.config.from_envvar('MSIA_SETTINGS', silent=True)

# Initialize the database
db = SQLAlchemy(application)
