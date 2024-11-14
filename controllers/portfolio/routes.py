import os

from . import portfolio_bp
from forms import ContactForm
from flask import render_template, flash, url_for, redirect, request
from utils.email_utils import send_admin_email, send_user_response_email
from models import db, User, Experience, Education, Skills, Language, Projects, Home
import bleach # For sanitizing HTML
from datetime import datetime
import requests


CURRENT_YEAR = datetime.now().year



@portfolio_bp.route('/', methods=['GET'] )
def home():
    home = Home.query.first()
    user = User.query.first()


    return render_template('portfolio/index.html',user=user, home=home, current_year=CURRENT_YEAR)


@portfolio_bp.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    subject = 'Email from Your Portfolio Contact Form'
    user = User.query.first()

    # Check for reCAPTCHA response
    recaptcha_response = request.form.get('g-recaptcha-response')
    secret_key = os.environ.get('RECAPTCHA_SECRET_KEY')
    data = {
        'secret': secret_key,
        'response': recaptcha_response
    }

    # Send the request to Google for verification
    verify_response = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
    result = verify_response.json()

    # Verify reCAPTCHA result before processing form
    if form.validate_on_submit() and result.get('success'):
        name = bleach.clean(form.name.data)
        email = bleach.clean(form.email.data)
        message = bleach.clean(form.message.data)

        # Flash success message
        flash('Message sent successfully', 'success')

        # Send emails
        send_admin_email(name=name, subject=subject, email=email, message=message)
        send_user_response_email(name=name, email=email, subject=subject)

        return redirect(url_for('portfolio_bp.contact'))
    else:
        # Handle reCAPTCHA or form validation errors
        if not result.get('success'):
            flash('Please complete the CAPTCHA to submit the form.', 'danger')
        for field, errors in form.errors.items():
            for error in errors:
                flash(f'Error in {field}: {error}', 'danger')

    return render_template('portfolio/contact.html', form=form, current_year=CURRENT_YEAR, user=user)


@portfolio_bp.route('/resume', methods=['GET']  )
def resume():
    education = Education.query.all()
    experience = Experience.query.all()
    skills = Skills.query.all()
    languages = Language.query.all()
    user = User.query.first()  # Add this line to get the dashboard

    return render_template('portfolio/resume.html', user=user,current_year=CURRENT_YEAR, all_education=education, all_experience=experience, all_skills=skills, all_languages=languages)


@portfolio_bp.route('/projects', methods=['GET'])
def projects():
    projects = Projects.query.all()
    user = User.query.first()

    return render_template('portfolio/projects.html', user=user,current_year=CURRENT_YEAR, all_projects=projects)

