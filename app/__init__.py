import flask_sqlalchemy
from flask import Flask
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object('flask_config')
db = flask_sqlalchemy.SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

from app import views, models
