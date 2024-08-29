from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_migrate import Migrate
import os
import logging

# Set up logging for debugging
logging.basicConfig(level=logging.INFO)

UPLOAD_FOLDER = 'static/uploads'

app = Flask(__name__)

# Configuration settings
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://luxeladies_user:IpZHnSqgL1Eh8bXZIo1fCtwLzYFH9Lk1@dpg-cr8acfaj1k6c73evj1ag-a/luxeladies'
app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'static/uploads')

# Session management settings
app.config['SESSION_COOKIE_NAME'] = 'session'
# app.config['SESSION_COOKIE_DOMAIN'] = '.luxeladies.co.uk'  # Replace with your domain
app.config['SESSION_COOKIE_SECURE'] = True  # Ensure cookies are only sent over HTTPS
app.config['REMEMBER_COOKIE_SECURE'] = True



db = SQLAlchemy(app)
migrate = Migrate(app, db)

bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

from app.models import User

@login_manager.user_loader
def load_user(user_id):
    logging.info(f"Loading user with ID: {user_id}")
    return User.query.get(int(user_id))

from app import routes
