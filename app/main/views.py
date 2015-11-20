from flask import render_template, redirect, url_for, abort, flash, request,\
    current_app, make_response, g, jsonify
from flask.ext.login import login_required, current_user
from flask.ext.sqlalchemy import get_debug_queries
from . import main
from .forms import SearchForm, FilterForm
from .. import db, moment
from ..models import User, Listing, Tax, School, Geo, Crime, School
from ..listingGenerator import generateListing

@main.before_app_request
def before_request():
    g.search = SearchForm()

@main.route('/search', methods=['GET','POST'])
def search():
    if g.search.validate_on_submit():
        return redirect(url_for('.report', address=g.search.search.data))
@main.route('/', methods=['GET', 'POST'])
def index():
    search = SearchForm()
    filters = FilterForm()
    if search.validate_on_submit():
        return redirect(url_for('.report', address=search.search.data))
    return render_template('index.html', search=search, filters=filters, searchbar=False)


@main.route('/report/<address>', methods=['GET', 'POST'])
def report(address):
    listing = generateListing(address)
    thumbNail = listing.images.first()
    tax_info = listing.tax_info.first()
    crime_info = listing.crime_info.first()
    geo_info = listing.geo_info.first()
    schools = listing.schools.first()
    imagePth = listing.images.first()
    return render_template('report.html', address=address,listing=listing, searchbar=True,
                            tax_info=tax_info, crime_info=crime_info,
                            geo_info=geo_info, schools=schools, imgPth=imagePth)
