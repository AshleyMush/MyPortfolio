from flask_wtf import FlaskForm
from flask_ckeditor import CKEditorField
from wtforms import StringField,DecimalField, SubmitField,SelectField, TextAreaField, PasswordField, BooleanField
from wtforms.validators import DataRequired,NumberRange, URL, Email, Length, ValidationError, InputRequired, Optional, EqualTo
import re
from flask import flash
from wtforms import SelectMultipleField
from wtforms.widgets import ListWidget, CheckboxInput
from utils.validators import PhoneNumberValidator


class ContactForm(FlaskForm):
    """
    Form for contact page
    """
    name = StringField(label='Name', validators=[DataRequired(), Length(max=64)],
                       render_kw={"placeholder": "Name",
                                  "class": "contact-form"})

    email = StringField(label='Email', validators=[DataRequired(), Email(message="You seem to be missing @ or .",
                                                                         check_deliverability=True)])


    message = TextAreaField(label='Message', validators=[DataRequired()],
                            render_kw={"placeholder": "Enter your message here",
                                       "class": "col-12"})

    submit = SubmitField(label='Send Message', render_kw={"class": "btn btn-dark col-12",
                                                          "id": "contact_submit_btn"})


class HomePageContentForm(FlaskForm):
    subheading  = StringField('Subheading')
    description = TextAreaField('Homepage Description', validators=[Optional()])
    img_url = StringField('Feature One Image URL', validators=[URL(message="Please enter a valid URL for the feature one image/video.")])
    submit = SubmitField('Save Changes')



class ProjectsPageForm(FlaskForm):
    thumbnail = StringField('Thumbnail Image URL', validators=[URL(message="Please enter a valid URL for the project thumbnail.")])
    title = StringField('Project Title', validators=[DataRequired()])
    description = CKEditorField('Project description')
    demo_link = StringField('Demo Link', validators=[URL(message="Please enter a valid URL for the project demo.")])
    repo_link = StringField('Repository Link', validators=[URL(message="Please enter a valid URL for the project repository.")])
    submit = SubmitField('Save Changes')

class ExperienceForm(FlaskForm):
    duration = StringField('Duration', validators=[DataRequired()])
    role = StringField('Role', validators=[DataRequired()])
    company = StringField('Company', validators=[DataRequired()])
    location = StringField('Location', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    submit = SubmitField('Save Changes')


class EducationForm(FlaskForm):
    duration = StringField('Duration', validators=[DataRequired()])
    institution = StringField('Institution', validators=[DataRequired()])
    qualification = StringField('Qualification', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    submit = SubmitField('Save Changes')

class SkillsForm(FlaskForm):
    name = StringField('Skill Name', validators=[DataRequired()])
    submit = SubmitField('Save Changes')

class LanguageForm(FlaskForm):
    name = StringField('Language Name', validators=[DataRequired()])
    submit = SubmitField('Save Changes')