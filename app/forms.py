from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, Optional, URL
from app import db

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = db.users.find_one({"username": username.data})
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = db.users.find_one({"email": email.data})
        if user:
            raise ValidationError('That email is already registered.')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class BookForm(FlaskForm):
    title = StringField('Book Title', validators=[DataRequired()])
    author = StringField('Author', validators=[DataRequired()])
    
    # CHANGED: Now asking for a Link (URL) instead of a File
    cover_photo = StringField('Cover Image URL', validators=[
        DataRequired(),
        URL(message="Please enter a valid Image URL starting with http:// or https://")
    ])

    # CHANGED: Now asking for a Link (URL) instead of a File
    pdf = StringField('PDF Download URL', validators=[
        DataRequired(),
        URL(message="Please enter a valid PDF URL starting with http:// or https://")
    ])

    genre = SelectField('Genre', choices=[
        ('Fiction', 'Fiction'),
        ('Non-Fiction', 'Non-Fiction'),
        ('Sci-Fi', 'Science Fiction'),
        ('Fantasy', 'Fantasy'),
        ('Mystery', 'Mystery'),
        ('Thriller', 'Thriller'),
        ('Romance', 'Romance'),
        ('Horror', 'Horror'),
        ('Biography', 'Biography'),
        ('History', 'History'),
        ('Self-Help', 'Self-Help'),
        ('Tech', 'Technology'),
        ('Other', 'Other (Specify below)')
    ], validators=[DataRequired()])

    custom_genre = StringField('If "Other", please specify:', validators=[Optional()])
    description = TextAreaField('Short Description (Optional)', validators=[Optional()])
    submit = SubmitField('Submit for Approval')

class RequestResetForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

    def validate_email(self, email):
        user = db.users.find_one({"email": email.data})
        if user is None:
            raise ValidationError('There is no account with that email. You must register first.')

class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')