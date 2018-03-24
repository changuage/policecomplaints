
from flask import Flask
from flask_sqlalchemy import SQLAlchemy


# needed by beanstalk
application = Flask(__name__)
application.config.from_object('config')

# Initialize the database
db = SQLAlchemy(application)
