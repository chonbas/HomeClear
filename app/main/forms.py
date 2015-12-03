from flask.ext.wtf import Form
from wtforms import StringField, TextAreaField, BooleanField, SelectField,\
    SubmitField, IntegerField
from wtforms.validators import Required, Length, Email, Regexp
from wtforms import ValidationError
from ..models import User

class SearchForm(Form):
    search = StringField('', validators=[Length(5,64)])

class FilterForm(Form):
    rooms = IntegerField('Bedrooms:')
    bathrooms = IntegerField('Bathrooms:')
    area = IntegerField('Min Square Feet:')
    min_price = IntegerField('Min Price:')
    max_price = IntegerField('Max Price:')
