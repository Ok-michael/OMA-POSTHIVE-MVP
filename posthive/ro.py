#!/usr/bin/env python3
from flask import render_template, flash, redirect, url_for
from posthive import app
from posthive.forms import RegistrationForm, LoginForm
from posthive.models import User, Post
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
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form) 
    
@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@blog.com' and form.password.data == 'password':
            flash('You have been logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)

