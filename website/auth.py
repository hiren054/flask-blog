from flask import Blueprint, render_template, url_for, redirect,flash, request
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, logout_user, login_required, current_user

auth = Blueprint('auth' , __name__)


@auth.route('/signup',methods = ['GET','POST'])
def signup():
    if request.method == 'POST' :
        name = request.form.get('name')
        email = request.form.get('email')      
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        user = User.query.filter_by(email=email).first()
        error = None

        if user :
            error = f"User {user.email.capitalize()} is already Registered."
        elif not name :
            error = 'Name is Required.'
        elif not email :
            error = "Email is Required."
        elif len(email) < 4 :
            error = "Email must be greater than 4 characters."
        elif len(password1) < 5 :
            error = "Password must be greater than 5 characters."
        elif not password1 :
            error = "Passsword is Required."
        elif password1 != password2 :
            error = "Password does not match."
        
        
        if error is None:
            new_user = User(email=email,name=name,
                    password = generate_password_hash(password1, method='sha256'))
            error = "Registration complete."
            flash(error)
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('auth.login'))

        flash(error)
    
    return render_template("signup.html", user=current_user)

@auth.route('/login', methods = ['GET','POST']) 
def login():
    if current_user.is_authenticated :
        return redirect(url_for('views.home'))
    if request.method == 'POST' :
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        error = None


        if user is None :
            error = "Incorrect Email"
        elif not check_password_hash(user.password, password) :
            error = "Incorrect Password"

        if error is None :
            login_user(user, remember=False)
            error = "Login Successfull."
            flash(error)
            return redirect(url_for('views.home'))

        flash(error)

    return render_template("login.html", user=current_user)


    #     user = User.query.filter_by(email=email).first()
    #     # print(user.id)
    #     if user :
    #         #checking the login form data and check with the database
    #         if check_password_hash(user.password, password) :
    #             print("login successfull")
    #             login_user(user, remember=False)
    #             return redirect(url_for('views.home'))
    #         else :
    #             print("incorrect password")
    #     else:
    #         print("email does not exist!")
    # return render_template("login.html", user=current_user)


@auth.route('/logout')
@login_required
def logout(): 
    logout_user()
    return redirect(url_for('views.home'))
