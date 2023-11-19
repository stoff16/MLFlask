from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from config import Config
import flask_sqlalchemy
from app import models, views, forms, routes
import MySQLdb
import mysql.connector
from flask import Flask, render_template, request, redirect, url_for, session, flash, Blueprint


# Créez une instance de l'application Flask
app = Flask(__name__, instance_relative_config=True)
main_bp = Blueprint('main', __name__)
app.config.from_object(Config)

# Configuration de l'application Flask
app.config['SECRET_KEY'] = '19581024'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:19581024@localhost/pythonlogin'

# Initialisation des extensions
db = SQLAlchemy(app)
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

