from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_migrate import Migrate

import os

UPLOAD_FOLDER = 'static/uploads'


app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:TAGVHayCSYn64hdD@mysql-rds-luxe-ladies-2gnt.cxa8ok6mgjo2.us-west-2.rds.amazonaws.com:3306/primarydb'

# Set the upload folder within the app directory
app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'static/uploads')

db = SQLAlchemy(app)
migrate = Migrate(app, db)  # Initialize Flask-Migrate

bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

from app.models import User

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

from app import routes
