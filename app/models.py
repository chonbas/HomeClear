from datetime import datetime
import hashlib, sys
from werkzeug.security import generate_password_hash, check_password_hash
from flask import current_app, redirect, flash, request, url_for
from flask.ext.login import UserMixin, AnonymousUserMixin
from . import db, login_manager, Whoosh



favorited_listings = db.Table('favorited_listings',
        db.Column('user_id', db.Integer, db.ForeignKey('users.id'), nullable=False),
        db.Column('listing_id', db.Integer, db.ForeignKey('listings.id'), nullable=False),
        db.PrimaryKeyConstraint('listing_id', 'user_id')
)

class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    name = db.Column(db.String(64))
    favorites = db.relationship('Listing',secondary=favorited_listings,
                                backref=db.backref('users',lazy='dynamic'), lazy='dynamic')

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

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Listing(db.Model):
    __tablename__ = 'listings'

    id = db.Column(db.Integer, primary_key=True)
    raw_add = db.Column(db.String(128), unique=True)
    street_address = db.Column(db.String(128))
    city = db.Column(db.String(64))
    state = db.Column(db.String(32))
    zipcode = db.Column(db.String(16))
    price = db.Column(db.String(32))
    area = db.Column(db.Integer)
    lot_area = db.Column(db.Integer)
    bedrooms = db.Column(db.Integer)
    bathrooms = db.Column(db.Integer)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    realtor = db.Column(db.String(64))
    built_in = db.Column(db.String(64))
    lati = db.Column(db.Float)
    longi = db.Column(db.Float)
    images = db.relationship('Image', backref='listing', lazy='dynamic') #tie images to specific listings
    tax_info = db.relationship('Tax', backref='listing', lazy='dynamic')
    crime_info = db.relationship('Crime', backref='listing', lazy='dynamic')
    geo_info = db.relationship('Geo', backref='listing', lazy='dynamic')
    schools = db.relationship('School', backref='listing', lazy='dynamic')

    def __repr__(self):
        return '{0}(address={1}area={2}schools={3})'.format(self.__class__.__name__, self.address, self.area, self.schools )

class Image(db.Model):
    __tablename__ = 'images'

    id = db.Column(db.Integer, primary_key=True)
    path = db.Column(db.String(64))
    img_count = db.Column(db.Integer)
    listing_id = db.Column(db.Integer, db.ForeignKey('listings.id'))

    def __repr__(self):
        return '(%s, %d)' %(self.path,self.img_count)


class Tax(db.Model):
    __tablename__ = 'taxes'

    id = db.Column(db.Integer, primary_key=True)
    last_sold_date = db.Column(db.String(32))
    last_sold_price = db.Column(db.String(32))
    property_tax_2014 = db.Column(db.Integer)
    property_tax_2013 = db.Column(db.Integer)
    property_tax_2012 = db.Column(db.Integer)
    property_tax_2011 = db.Column(db.Integer)
    property_tax_2010 = db.Column(db.Integer)

    tax_assesment_2014 = db.Column(db.Integer)
    tax_assesment_2013 = db.Column(db.Integer)
    tax_assesment_2012 = db.Column(db.Integer)
    tax_assesment_2011 = db.Column(db.Integer)
    tax_assesment_2010 = db.Column(db.Integer)
    listing_id = db.Column(db.Integer, db.ForeignKey('listings.id'))


class School(db.Model):
    __tablename__ = 'schools'

    id = db.Column(db.Integer, primary_key=True)
    school_district = db.Column(db.String(64))
    elementary_school = db.Column(db.String(64))
    middle_school = db.Column(db.String(64))
    high_school = db.Column(db.String(64))
    university = db.Column(db.String(64))
    listing_id = db.Column(db.Integer, db.ForeignKey('listings.id'))

    def __repr__(self):
        return 'elem = {0} high = {1}'.format(self.elementarySchool, self.highSchool)

class Crime(db.Model):
    __tablename__ = 'crimes'

    id = db.Column(db.Integer, primary_key=True)
    violent_crime_rate = db.Column(db.Float)
    property_crime_rate = db.Column(db.Float)
    crime_per_mile = db.Column(db.Float)
    listing_id = db.Column(db.Integer, db.ForeignKey('listings.id'))

    def __repr__(self):
        return '(rate = {0} graph = {1}'.format(self.rate, self.graph)

class Geo(db.Model):
    __tablename__ = 'geos'

    id = db.Column(db.Integer, primary_key=True)
    most_frequent_incident = db.Column(db.String(64))
    most_recent_incident = db.Column(db.String(64))
    geo_distance = db.Column(db.String(64))
    epicenter_lat = db.Column(db.Float)
    epicenter_long = db.Column(db.Float)
    listing_id = db.Column(db.Integer, db.ForeignKey('listings.id'))


#solely for injecting data into db
class Inject():
    def injectData(self):
        import locale, urllib2, json,os
        locale.setlocale( locale.LC_ALL, '' )

        f = open("app/data/listings.txt", 'r')
        basedir = os.path.abspath(os.path.dirname(__file__))

        for line in f:
            toks = line.split(';')
            print(line)
            linToks = [s.strip() for s in toks]
            linToks = [s.replace(',','') for s in linToks]
            raw_add = " ".join(linToks[1:5])
            add = urllib2.quote(raw_add)
            geocode_url = "https://maps.googleapis.com/maps/api/geocode/json?address=%s&sensor=false&region=us" %add
            req = urllib2.urlopen(geocode_url)
            jsonResponse = json.loads(req.read())
            coordinates = jsonResponse['results'][0]['geometry']['location']
            lati = coordinates['lat']
            longi = coordinates['lng']
            last_sold_price = linToks[13]
            if (last_sold_price != "N/A"):
                last_sold_price = locale.currency( int(last_sold_price), grouping=True )
            newListing = Listing(raw_add = raw_add, street_address = linToks[1],
                            city = linToks[2], state=linToks[3],zipcode=linToks[4],
                            price=locale.currency( int(linToks[9]), grouping=True ), area=linToks[5], lot_area=linToks[6],
                            bedrooms=linToks[7], bathrooms=linToks[8], realtor=linToks[10],
                            built_in=linToks[11], lati=lati, longi=longi)
            newTax = Tax(last_sold_date=linToks[12],last_sold_price=last_sold_price,
                        property_tax_2014=linToks[14], property_tax_2013=linToks[15],
                        property_tax_2012=linToks[16],property_tax_2011=linToks[17],
                        property_tax_2010=linToks[18], tax_assesment_2014=linToks[19],
                        tax_assesment_2013=linToks[20],tax_assesment_2012=linToks[21],
                        tax_assesment_2011=linToks[22], tax_assesment_2010=linToks[23],
                        listing=newListing)
            imgPth = linToks[4] + "/" + linToks[0] + "/"
            list_dir = os.listdir(basedir+"/static/images/houses/"+imgPth)
            img_count = 0
            for file in list_dir:
                if file.endswith('.jpg'): # eg: '.txt'
                    img_count += 1
            images = Image(path=imgPth, listing=newListing, img_count=img_count)
            zipCode = linToks[4]
            elementary_school = middle_school = high_school=""
            violent_crime_rate = 0.87
            property_crime_rate = 22.45
            crime_per_mile = 65
            if zipCode == "94301":
                elementary_school="Addison Elementary School"
                middle_school="Jordan Middle School"
                high_school="Palo Alto High School"
            elif zipCode == "94303":
                elementary_school="Duveneck Elementary School"
                middle_school="Jordan Middle School"
                high_school="Palo Alto High School"
            elif zipCode == "94305":
                elementary_school="Escondido Elementary School"
                middle_school="J L Stanford Middle School"
                high_school="Palo Alto High School"
            elif zipCode == "94306":
                elementary_school="Barron Park Elementary School"
                middle_school="Terman Middle School"
                high_school="Henry M. Gunn High School"
            if (newListing.city == "East Palo Alto"):
                violent_crime_rate = 12.08
                property_crime_rate = 20.76
                crime_per_mile = 384
            school = School(school_district="Palo Alto Unifed School District", elementary_school=elementary_school,
                            middle_school=middle_school, high_school=high_school, university="Stanford University",listing=newListing)
            crime = Crime(violent_crime_rate=violent_crime_rate, property_crime_rate=property_crime_rate,
                    crime_per_mile=crime_per_mile,listing=newListing)
            most_frequent_incident="Earthquakes"
            most_recent_incident="11/22/2015 - 1.6 Magnitude Earthquake, 6km Depth, Near East Foothills, CA"
            geo_distance = "33.2km from Palo Alto, CA"
            epicenter_lat = 37.414
            epicenter_long = -121.762
            geo = Geo(most_frequent_incident=most_frequent_incident, most_recent_incident=most_recent_incident,
                        geo_distance=geo_distance, epicenter_long=epicenter_long, epicenter_lat=epicenter_lat,listing=newListing)
            db.session.add(newListing)
            db.session.add(newTax)
            db.session.add(images)
            db.session.add(school)
            db.session.add(crime)
            db.session.add(geo)
        db.session.commit()
        f.close()
