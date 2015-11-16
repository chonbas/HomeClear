from datetime import datetime
import hashlib, sys
from werkzeug.security import generate_password_hash, check_password_hash
from markdown import markdown
import bleach
from flask import current_app, request, url_for
from flask.ext.login import UserMixin, AnonymousUserMixin
from . import db, login_manager, Whoosh

class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    name = db.Column(db.String(64))
    #favorites reference

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def is_adminitrator(self):
        return self.admin

    def ping(self):
        self.last_seen = datetime.utcnow()
        db.session.add(self)

class AnonymousUser(AnonymousUserMixin):



login_manager.anonymous_user = AnonymousUser

@login_manager.user_loader
def load_user(user_id):
    return User.quer.get(int(user_id))

#TABLE FOR FAVORITING REFERENCES

class Listing(db.Model):
    __tablename__ = 'listings'
    __searchable__ = ['address']

    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(128))
    bedrooms = db.Column(db.Integer)
    bathrooms = db.Column(db.Integer)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    seller = db.Column(db.String(64))
        
