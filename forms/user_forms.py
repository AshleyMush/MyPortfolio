from flask_wtf import FlaskForm
from flask_ckeditor import CKEditorField
from wtforms import StringField,DecimalField, SubmitField,SelectField, TextAreaField, PasswordField, BooleanField
from wtforms.validators import DataRequired,NumberRange, URL, Email, Length, ValidationError, InputRequired, Optional, EqualTo
import re
from flask import flash
from wtforms import SelectMultipleField
from wtforms.widgets import ListWidget, CheckboxInput
from utils.validators import PhoneNumberValidator


class SocialMediaInfoForm(FlaskForm):
    hackerrank = StringField('HackerRank')
    github = StringField('Github')
    linkedin = StringField('LinkedIn')
    facebook = StringField('Facebook')
    instagram = StringField('Instagram')
    submit = SubmitField('Save')

class UpdateEmailForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Save')

class UpdatePhoneForm(FlaskForm):
    phone_number = StringField(
        'Phone Number',
        validators=[
            DataRequired(message="Phone number is required."),
            PhoneNumberValidator  # Use the custom validator
        ]
    )
    submit = SubmitField('Save')



class ChangePasswordForm(FlaskForm):
    current_password = PasswordField('Current Password', validators=[DataRequired(), Length(min=8)])
    new_password = PasswordField('New Password', validators=[DataRequired(), Length(min=8)])
    confirm_new_password = PasswordField('Confirm New Password', validators=[
        DataRequired(),
        EqualTo('new_password', message='Passwords must match.')
    ])
    submit = SubmitField('Change Password')



class RegisterForm(FlaskForm):
    first_name = StringField("First Name", validators=[DataRequired()])
    last_name = StringField("Last Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[
        DataRequired(),
        Length(min=8, message="Password must be at least 8 characters long")
    ])
    confirm_password = PasswordField("Repeat Password", validators=[
        DataRequired(),
        EqualTo('password', message="Passwords must match")
    ])
    submit = SubmitField("Register")


class AboutMeForm(FlaskForm):
    about = TextAreaField('About Me', validators=[DataRequired(), Length(max=1000)])
    submit = SubmitField('Save')


