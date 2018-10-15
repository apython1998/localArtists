from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import StringField, TextAreaField, PasswordField, BooleanField, DateField, \
    SelectField, SelectMultipleField, SubmitField
from wtforms.validators import DataRequired, EqualTo, Email, Length, ValidationError
from app.models import User


class NewArtistForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(max=64)])
    hometown = StringField('Hometown', validators=[DataRequired(), Length(max=64)])
    description = TextAreaField('Description', validators=[DataRequired(), Length(max=256)])
    submit = SubmitField('Submit')


class NewVenueForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(max=64)])
    address = StringField('Address', validators=[DataRequired(), Length(max=256)])
    submit = SubmitField('Submit')


class NewEventForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(max=128)])
    time = DateField('Start Time', format='%m/%d/%Y', id='timepick')
    venue = SelectField('Venue', coerce=int)
    artists = SelectMultipleField('Artists', coerce=int)
    submit = SubmitField('Submit')


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')  # text that goes in the button


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')  # text that goes in the button

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Username Taken! Please use a different username...')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Email in use! Please use a different email...')


class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    about_me = TextAreaField('About me', validators=[Length(min=0, max=140)])
    submit = SubmitField('Submit')  # text that goes in the button

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None and user.username is not current_user.username:
            raise ValidationError('Username Taken! Please use a different username...')
