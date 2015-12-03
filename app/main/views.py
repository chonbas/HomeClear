from flask import render_template, redirect, url_for, abort, flash, request,\
    current_app, make_response, g, jsonify, session
from flask.ext.login import login_required, current_user
from flask.ext.sqlalchemy import get_debug_queries
from . import main
from .forms import SearchForm, FilterForm
from .. import db, moment
from ..models import User, Listing, Tax, School, Geo, Crime, School
from ..listingGenerator import generateListing
import usaddress, urllib2, json

@main.before_request
def before_request():
    g.search = SearchForm()
    g.filters = FilterForm()

@main.route('/search', methods=['GET','POST'])
def search():
    if g.search.validate_on_submit():
        query = g.search.search.data
        return searchParse(query)

@main.route('/favorites/', methods=['GET', 'POST'])
def favorites():
    if current_user.is_authenticated:
        listings = list(current_user.favorites)
    else:
        listings=[]
        if 'favorites' in session:
            for listing_id in session['favorites']:
                listing = Listing.query.get_or_404(listing_id)
                listings.append(listing)
        else:
            session['favorites'] = {}
    return render_template('listings.html', favs=True,listings=listings, search=g.search, searchbar=True, count=len(listings))

@main.route('/favorite/<int:listing_id>', methods=['GET', 'POST'])
def favorite(listing_id):
    listing = Listing.query.get_or_404(listing_id)
    if current_user.is_authenticated:
        if listing is not None:
            current_user.favorites.append(listing)
    else:
        if 'favorites' in session:
            session['favorites'][listing_id]=True
        else:
            session['favorites'] = {}
            session['favorites'][listing_id]=True
    return redirect(request.args.get('next') or request.referrer or url_for('main.index'))

@main.route('/unfavorite/<int:listing_id>', methods=['GET', 'POST'])
def unfavorite(listing_id):
    listing = Listing.query.get_or_404(listing_id)
    if current_user.is_authenticated:
        if listing is not None:
            current_user.favorites.remove(listing)
    else:
        if 'favorites' in session:
            del session['favorites'][str(listing_id)]
        else:
            session['favorites'] = {}
    return redirect(request.args.get('next') or request.referrer or url_for('main.index'))

@main.route('/', methods=['GET', 'POST'])
def index():
    if g.search.validate_on_submit():
        query = g.search.search.data
        filters = {'bedrooms':g.filters.}
        return searchParse(query)
    return render_template('index.html', search=g.search, filters=g.filters, searchbar=False)


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
@main.route('/lots/<address>', methods=['GET','POST'])
def lots(address):
    parsed = usaddress.tag(address)[0]
    listings =[]
    if 'ZipCode' in parsed:
        listings = list(Listing.query.filter_by(zipcode=parsed['ZipCode']).order_by(Listing.timestamp.desc()))
    elif 'PlaceName' and 'StateName' in parsed:
        if 'StreetNamePreDirectional' and 'StreetName' in parsed:
            parsed['PlaceName'] = parsed['StreetNamePreDirectional'] + " " + parsed['StreetName'] + " " + parsed['PlaceName']
        listings = list(Listing.query.filter_by(city=parsed['PlaceName'],state=parsed['StateName']).order_by(Listing.timestamp.desc()))
    else:
        flash('Please enter a valid address including either a zipcode or city name and state.')
    for listing in listings:
        if listing.lot_area == 'N/A':
            listings.remove(listing)
    return render_template('listings.html', query=address,lots=True,address=address, favs=False, search=g.search, searchbar=True,listings=listings,count=len(listings))

@main.route('/listings/<address>', methods=['GET', 'POST'])
def listings(address):
    parsed = usaddress.tag(address)[0]
    listings =[]
    if 'ZipCode' in parsed:
        listings = list(Listing.query.filter_by(zipcode=parsed['ZipCode']).order_by(Listing.timestamp.desc()))
    elif 'PlaceName' and 'StateName' in parsed:
        if 'StreetNamePreDirectional' and 'StreetName' in parsed:
            parsed['PlaceName'] = parsed['StreetNamePreDirectional'] + " " + parsed['StreetName'] + " " + parsed['PlaceName']
        listings = list(Listing.query.filter_by(city=parsed['PlaceName'],state=parsed['StateName']).order_by(Listing.timestamp.desc()))
    else:
        flash('Please enter a valid address including either a zipcode or city name and state.')
    print g.filters.rooms.data
    return render_template('listings.html',query=address, lots=False,address=address,favs=False,search=g.search, searchbar=True, listings=listings, count=len(listings))

#Function to take a query and return either report or listings
def searchParse(query):
    parsed = usaddress.tag(query) # returns tuple with parsed string and 'street address' or 'ambiguous'
    if parsed[1] == 'Street Address':
        return redirect(url_for('.report', address=query))
    else:
        return redirect(url_for('.listings', address=query))
