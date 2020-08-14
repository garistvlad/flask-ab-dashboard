from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField, TextAreaField, BooleanField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError, Optional
from wtforms.fields.html5 import DateField

from models import ABExperiment, ABOption, User, App


class ABExperimentForm(FlaskForm):
    app = SelectField("App", choices=[(i.id, i.name) for i in App.query.all()], coerce=int)
    exp_name = StringField('Experiment Name', validators=[DataRequired()])
    description = TextAreaField('Short Description', validators=[DataRequired()])
    start_date = DateField("Start Date", validators=[DataRequired()], format="%Y-%m-%d")
    end_date = DateField("End Date", validators=[Optional()], format="%Y-%m-%d") # may be empty
    
    ### Options ###
    # control
    option_control1 = StringField('Control option #1', validators=[DataRequired()])
    option_control2 = StringField('Control option #2', validators=[Optional()])
    option_control3 = StringField('Control option #3', validators=[Optional()])
    # test
    option_test1 = StringField('Test option #1', validators=[DataRequired()])
    option_test2 = StringField('Test option #2', validators=[Optional()])
    option_test3 = StringField('Test option #3', validators=[Optional()])


class UserForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    is_admin = BooleanField("Admin?")
