from flask_wtf import Form
from wtforms import TextField, IntegerField, TextAreaField, SubmitField, RadioField, SelectField

from wtforms import validators, ValidationError

class SearchForm(Form):
	name = TextField("Name Of Person",[validators.Required("Please enter a name to search.")])
	submit = SubmitField("Send")
