from flask import render_template, redirect, url_for, abort, flash, request,\
    current_app, make_response, g, jsonify
from flask.ext.login import login_required, current_user
from flask.ext.sqlalchemy import get_debug_queries
from . import main
from .forms import SearchForm, FilterForm
from .. import db, moment
from ..models import User, Listing, Tax, School, Geo, Crime, School
from ..listingGenerator import generateListing
import usaddress, urllib2, json

@main.before_app_request
def before_request():
    g.search = SearchForm()

@main.route('/search', methods=['GET','POST'])
def search():
    if g.search.validate_on_submit():
        query = g.search.search.data
        return searchParse(query)

@main.route('/', methods=['GET', 'POST'])
def index():
    search = SearchForm()
    filters = FilterForm()
    if search.validate_on_submit():
        query = search.search.data
        return searchParse(query)
    return render_template('index.html', search=search, filters=filters, searchbar=False)


@main.route('/report/<address>', methods=['GET', 'POST'])
def report(address):
    add = urllib2.quote(address)
    geocode_url = "https://maps.googleapis.com/maps/api/geocode/json?address=%s&sensor=false&region=us" %add
    req = urllib2.urlopen(geocode_url)
    jsonResponse = json.loads(req.read())
    coordinates = jsonResponse['results'][0]['geometry']['location']
    lati = coordinates['lat']
    longi = coordinates['lng']
    listing = Listing.query.filter_by(lati=lati, longi=longi).first()
    if listing is None:
        flash("Unable to find a listing matching this address.")
        return redirect(url_for('.index'))
    tax_info = listing.tax_info.first()
    crime_info = listing.crime_info.first()
    geo_info = listing.geo_info.first()
    schools = listing.schools.first()
    imagePth = listing.images.first()
    return render_template('report.html', address=address,listing=listing, searchbar=True,
                            tax_info=tax_info, crime_info=crime_info,
                            geo_info=geo_info, schools=schools, imgPth=imagePth)

@main.route('/listings/<address>', methods=['GET', 'POST'])
def listings(address):
    parsed = usaddress.tag(address)[0]
    listings =[]
    if 'ZipCode' in parsed:
        listings = Listing.query.filter_by(zipcode=parsed['ZipCode']).order_by(Listing.timestamp.desc())
    elif 'PlaceName' and 'StateName' in parsed:
        listings = Listing.query.filter_by(city=parsed['PlaceName'],state=parsed['StateName']).order_by(Listing.timestamp.desc())
    else:
        flash('Please enter a valid address including either a zipcode or city name and state.')
    return render_template('listings.html', search=g.search, searchbar=True, listings=listings, count=listings.count())

#Function to take a query and return either report or listings
def searchParse(query):
    parsed = usaddress.tag(query) # returns tuple with parsed string and 'street address' or 'ambiguous'
    if parsed[1] == 'Street Address':
        return redirect(url_for('.report', address=query))
    else:
        return redirect(url_for('.listings', address=query))
