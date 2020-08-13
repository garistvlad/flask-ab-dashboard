from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError

from models import User


class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    password2 = PasswordField('Confirm password', validators=[DataRequired(), EqualTo("password")])

    def validate_email(self, field):
        # authorized domain zone
        if field.data.strip().split("@")[-1] not in ["pay-s.ru", "pays.ru", "bip.ru", "mpp-rus.ru"]:
            raise ValidationError(message="Wrong email domain. Please, contact v.garist to request an access.")

        # user is already exists
        user = User.query.filter_by(email=field.data.strip()).first()
        if user is not None:
            raise ValidationError(message=f"Email: '{user.name}' is already registered. Choose another one.")



class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
