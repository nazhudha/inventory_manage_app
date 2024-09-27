from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# Initialize extensions without attaching them to the app yet
db = SQLAlchemy()
login_manager = LoginManager()
