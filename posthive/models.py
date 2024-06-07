#!/usr/bin/env python3
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from posthive import db

class User(db.Model):
    """This class represents the Users and holds all the relevant attributes
    our user must have to be stored in the database

    Args:
        db (db.Model): it inherits from the db.Mode classes

    Returns:
        None
    """

    id = db.Column(db.Integer, primary_key=True) 
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)

    def __repr__(self):
        """ this class represents a the class in a nicely formatted string

        Returns:
            _type_: String rep of the class
        """
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"
    
class Post(db.Model):
    """This class is used to represent the Posts and it has all the 
    fields needed for our posts to be included in our database

    Args:
        db.Model: this class inherits from the db.Model class

    Returns:
        None
    """

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    def __repr__(self):
        """this method gives a string representation for the post class

        Returns:
            String: representative of this class in a nicely formatted
            way
        """
        return f"Post('{self.title}', '{self.date_posted}')"
