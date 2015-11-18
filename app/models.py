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

class AnonymousUser(AnonymousUserMixin):


login_manager.anonymous_user = AnonymousUser

@login_manager.user_loader
def load_user(user_id):
    return User.quer.get(int(user_id))

#TABLE FOR FAVORITING REFERENCES

schools_homes = db.Table('schools_homes',
        db.Column('school_id', db.Integer, db.ForeignKey('schools.id'), nullable=False),
        db.Column('listing_id', db.Integer, db.ForeignKey('listings.id'), nullable=False),
        db.PrimaryKeyConstraint('listing_id', 'school_id')
)


class Listing(db.Model):
    __tablename__ = 'listings'
    __searchable__ = ['address']

    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(128), unique=True)
    area = db.Column(db.Integer)
    bedrooms = db.Column(db.Integer)
    bathrooms = db.Column(db.Integer)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    seller = db.Column(db.String(64))
    images = db.relationship('Image', backref='listing', lazy='dynamic') #tie images to specific listings
    tax_info = db.relationship('Tax', backref='listing', lazy='dynamic')
    crime_info = db.relationship('Crime', backref='listing', lazy='dynamic')
    schools = db.relationship('School', secondary=schools_homes,
                                backref=db.backref('listings', lazy='dynamic'))

    def __repr__(self):
        return '{0}(address={1})'.format(self.__class__.__name__, self.address)

class Image(db.Model):
    __tablename__ = 'images'

    id = db.Column(db.Integer, primary_key=True)
    path = db.Column(db.String(128), unique=True)
    listing_id = db.Column(db.Integer, db.ForeignKey('listings.id'))

    def __repr__(self):
        return '(%s)' %self.path


class Tax(db.Model):
    __tablename__ = 'taxes'

    id = db.Column(db.Integer, primary_key=True)
    rate = db.Column(db.Integer)
    graph = db.Column(db.String(128)) #path to graph
    listing_id = db.Column(db.Integer, db.ForeignKey('listings.id'))

    def __repr__(self):
        return '(rate = {0} graph = {1}'.format(self.rate, self.graph)

class School(db.Model):
    __tablename__ = 'schools'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))

    def __repr__(self):
        return '(%s)' %self.name

class Crime(db.Model):
    __tablename__ = 'crimes'

    id = db.Column(db.Integer, primary_key=True)
    rate = db.Column(db.Integer)
    graph = db.Column(db.String(128)) #path to graph
    listing_id = db.Column(db.Integer, db.ForeignKey('listings.id'))

    def __repr__(self):
        return '(rate = {0} graph = {1}'.format(self.rate, self.graph)
