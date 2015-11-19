from flask import render_template, redirect, url_for, abort, flash, request,\
    current_app, make_response, g
from flask.ext.login import login_required, current_user
from flask.ext.sqlalchemy import get_debug_queries
from . import main
from .forms import SearchForm, FilterForm
from .. import db, Whoosh
from ..models import User, Listing

@main.before_app_request
def before_request():
    g.search = SearchForm()

@main.route('/', methods=['GET', 'POST'])
def index():
    search = SearchForm()
    filters = FilterForm()
    if search.validate_on_submit():
        search_string = search.search.data
        return redirect(url_for('main.report', address=search_string))
    return render_template('index.html', search=search, filters=filters, searchbar=False)

@main.route('/report/<address>', methods=['GET', 'POST'])
def report(address):
    return render_template('report.html', search_string=address, searchbar=True)
