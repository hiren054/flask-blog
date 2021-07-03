from flask_login import UserMixin
from website import db
from datetime import datetime
from sqlalchemy import column, Integer , String
 
class User(db.Model,UserMixin) :
    id = db.Column(db.Integer, primary_key= True)
    name = db.Column(db.String(150), nullable= False)
    email = db.Column(db.String(150), unique= True, nullable= False)
    password = db.Column(db.String(150), nullable= False)
    posts = db.relationship('Post', backref= 'author')  

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable= False)
    content = db.Column(db.String(5000), nullable= False)
    created = db.Column(db.DateTime, default=datetime.now(), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable= False)  





    
   
