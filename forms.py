from flask_wtf import FlaskForm
from wtforms import TextField, IntegerField, TextAreaField, SubmitField, RadioField, SelectField, BooleanField

from wtforms import validators, ValidationError
from wtforms.validators import Required, EqualTo, Optional

class RequiredIf(Required):
    # a validator which makes a field required if
    # another field is set and has a truthy value

    def __init__(self, other_field_name, *args, **kwargs):
        self.other_field_name = other_field_name
        super(RequiredIf, self).__init__(*args, **kwargs)

    def __call__(self, form, field):
        other_field = form._fields.get(self.other_field_name)
        if other_field is None:
            raise Exception('no field named "%s" in form' % self.other_field_name)
        if bool(other_field.data):
            super(RequiredIf, self).__call__(form, field)


class SearchForm(FlaskForm):
	name = TextField("Name Of Person",[validators.Required("Please enter a name to search.")])
	submit = SubmitField("Search")


class LetterForm(FlaskForm):
	name = TextField("Name Of Person",[validators.Required("Please enter a name to search.")])
	wrote = BooleanField("Wrote")
	received = BooleanField("Recieved",validators=[RequiredIf('wrote')])        
	submit = SubmitField("Search")
	
class TravelForm(FlaskForm):
	date = IntegerField("Date",[validators.Required("Please enter a name to search.")])
	submit = SubmitField("Search")

class OrgForm(FlaskForm):
	name = TextField("Name Of Affiliation",[validators.Required("Please enter a name to search.")])
	submit = SubmitField("Search")
