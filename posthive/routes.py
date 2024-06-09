#!/usr/bin/env python3
from flask import request, render_template, flash, redirect, url_for
from posthive import app, db, bcrypt
from posthive.forms import RegistrationForm, LoginForm, UpdateAccountForm
from posthive.models import User, Post
from flask_login import login_user, logout_user, current_user, login_required

posts = [
    {
        'author': 'Michael Oko',
        'title': 'first_post',
        'content': 'Just a dummy for the first_post',
        'date_posted': 'June 2, 2024'
    },
    {
        'author': 'Corey Schafer',
        'title': 'Second_post',
        'content': 'Just a dummy for the second_post',
        'date_posted': 'June 3, 2024'
    },
    {
        'author': 'Sylvanus Oko',
        'title': 'third_post',
        'content': 'Just a dummy for the third_post',
        'date_posted': 'June 4, 2024'
    }
]

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', posts=posts)

@app.route('/about')
def about():
    return render_template('about.html', title='about')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        user = User(
            username=form.username.data,
            email = form.email.data,
            password = hashed_password
        )
        db.session.add(user)
        db.session.commit()
        flash("Your account has been created, you're now able to log in", 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form) 
    
@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if  next_page else redirect(url_for('home'))
        flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
  form = UpdateAccountForm()
  if form.validate_on_submit():
      current_user.username = form.username.data
      current_user.email = form.email.data
      db.session.commit()
      flash('Account has been update', 'success')
      return redirect(url_for('account'))
  elif request.method == 'GET':
      form.username.data = current_user.username
      form.email.data = current_user.email
  image_file = url_for('static', 
    filename='profile_pics/' + current_user.image_file)
  return render_template('account.html', 
        title='account', image_file=image_file, form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))