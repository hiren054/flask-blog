from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager


db = SQLAlchemy()
DB_NAME = "user.db"          

#setting up create app like to work as a python pacake 
def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'Jay Yogeshwar'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)         #intialize the database

    #importing both blueprint from auth and views.py files
    from .views import views
    from .auth import auth
    from .errors import errors

    #registering blueprint
    app.register_blueprint(views,url_prefix='/')
    app.register_blueprint(auth,url_prefix='/')
    app.register_blueprint(errors,url_prefix='/')

    from .models import User, Post

    create_database(app)


    # Here we use a class of some kind to represent and validate our
    #initialize the user that has alreay login or not   
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app

def create_database(app):
    #check if database is exists or if not exists create the database
    if not path.exists('website/' + DB_NAME) : 
        db.create_all(app=app)
        print("databse created!")
