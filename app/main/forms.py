from flask.ext.wtf import Form
from wtforms import StringField, TextAreaField, BooleanField, SelectField,\
    SubmitField, IntegerField
from wtforms.validators import Required, Length, Email, Regexp
from wtforms import ValidationError
from ..models import User

class SearchForm(Form):
    search = StringField('', validators=[Length(5,64)])
    submit = SubmitField('Search')
    min_rooms = StringField('Min Bedrooms:')
    max_rooms = StringField('Max Bedrooms:')
    min_bathrooms = StringField('Min Bathrooms:')
    max_bathrooms = StringField('Max Bathrooms:')
    min_area = StringField('Min Square Feet:')
    max_area = StringField('Max Square Feet:')
    min_price = StringField('Min Price:')
    max_price = StringField('Max Price:')
