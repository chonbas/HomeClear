from flask import render_template, redirect, url_for, abort, flash, request,\
    current_app, make_response, g
from flask.ext.login import login_required, current_user
from flask.ext.sqlalchemy import get_debug_queries
from . import main
from .forms import SearchForm
from .. import db, Whoosh
from ..models import User, Listing

@main.route('/', methods=['GET', 'POST'])
def index():
    form = SearchForm()
    return render_template('index.html', form=form)
