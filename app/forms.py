from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, Optional
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
    
    # 1. Cover Photo (Images only)
    cover_photo = FileField('Cover Photo', validators=[
        FileRequired(),
        FileAllowed(['jpg', 'png', 'jpeg'], 'Images only!')
    ])

    # 2. PDF Upload
    pdf = FileField('Upload PDF', validators=[
        FileRequired(),
        FileAllowed(['pdf'], 'PDFs only!')
    ])

    # 3. Genre Dropdown
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

    # 4. Custom Genre (Only used if 'Other' is selected)
    custom_genre = StringField('If "Other", please specify:', validators=[Optional()])

    # 5. Description (Optional)
    description = TextAreaField('Short Description (Optional)', validators=[Optional()])

    submit = SubmitField('Submit for Approval')