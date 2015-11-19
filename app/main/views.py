from flask import render_template, redirect, url_for, abort, flash, request,\
    current_app, make_response, g
from flask.ext.login import login_required, current_user
from flask.ext.sqlalchemy import get_debug_queries
from . import main
from .forms import SearchForm, FilterForm
from .. import db, moment
from flask.ext.googlemaps import Map
from ..models import User, Listing
from ..listingGenerator import generateListing

@main.before_app_request
def before_request():
    g.search = SearchForm()

@main.route('/search', methods=['POST'])
def search():
    return redirect(url_for('main.report', address=g.search.search.data))

@main.route('/', methods=['GET', 'POST'])
def index():
    search = SearchForm()
    filters = FilterForm()
    if search.validate_on_submit():
        return redirect(url_for('.report', address=search.search.data))
    return render_template('index.html', search=search, filters=filters, searchbar=False)


@main.route('/report/<address>', methods=['GET', 'POST'])
def report(address):
    sndmap = Map(
        identifier="sndmap",
        lat=37.4419,
        lng=-122.1419,
        markers=[(37.4419, -122.1419)],
        style="height:100%;width:100%;margin:0"
    )
    listing = generateListing(address)
    return render_template('report.html', listing=listing, searchbar=True, map=sndmap)
