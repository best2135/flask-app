from flask import Blueprint,render_template,request,flash,redirect,url_for
from . import db 
from .model import User,Note
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import login_user,logout_user,login_required,current_user


auth = Blueprint("auth",__name__)

@auth.route("/login",methods = ['GET','POST'])
def login():
    if request.method == "POST":
        email= request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password,password):
                flash("Account Logged in Successfully",category='success')
                login_user(user,remember=True)
                return redirect(url_for('views.home'))
            else:
                flash("Invalid password",category="error")
        else:
            flash("Email does not exist.",category="error")

    return render_template("login.html",user=current_user)

@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login')) 
@auth.route("/signup",methods = ['GET','POST'])
def signup():
     if request.method == "POST": 
        name = request.form.get("firstName")
        password1 = request.form.get('password1')
        password2 = request.form.get("password2")
        email = request.form.get('email')
       
        user = User.query.filter_by(email=email).first()
        if user:
            flash("Email Already exists!",category='error')
        elif len(email) < 4 :
            flash("email must be greater than 4 charecters",category = 'error')
        elif password1 != password2:
            flash("password is not same bro",category = 'error')
        elif len(password1) < 7:
            flash("passwor lesser than 7 char bro",category = 'error')
        elif len(name) < 2:
            flash("who named u :skull:",category = 'error')
        else:
           new_user =  User(name=name,email=email,password=generate_password_hash(password1,method='pbkdf2:sha256'))#wow sha256 hashing method is used in bitcoin too btw
           db.session.add(new_user)
           db.session.commit()
           login_user(new_user,remember=True)
           flash("Acount Created!",category='success')
           return redirect(url_for('views.home'))

     
     return render_template("signup.html",user=current_user)
