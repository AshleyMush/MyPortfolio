from flask import render_template, redirect, url_for, flash, request, session
from flask_login import current_user, login_required
from utils.decorators import roles_required
from utils.decorators import  nocache
from datetime import date
from utils.email_utils import send_approval_message, send_demotion_message
from . import dashboard_bp
from models import db, User, Experience, Education, Skills, Language, Projects, Home
from utils.encryption import check_password_hash, generate_password_hash
from forms import HomePageContentForm, ProjectsPageForm, ExperienceForm,  UpdateEmailForm\
    , SocialMediaInfoForm,UpdatePhoneForm, ChangePasswordForm, AboutMeForm\
    , EducationForm, SkillsForm, LanguageForm, ProjectsPageForm, EducationForm\
    , ExperienceForm, AboutMeForm, ContactForm


@dashboard_bp.app_context_processor
def inject_home_content_status():
    home_exists = Home.query.count() > 0
    return {'home_exists': home_exists}



@dashboard_bp.route('/add-home-content', methods=['GET', 'POST'])
@roles_required('Admin')
def add_home_content():
    """
    This function adds a home page content to the database
    """
    form = HomePageContentForm()
    if form.validate_on_submit():
        try:
            # Create a new instance of Home and add it to the database
            new_home_content = Home(
                subheading=form.subheading.data,
                description=form.description.data,
                img_url=form.img_url.data
            )
            db.session.add(new_home_content)
            db.session.commit()
            flash('Home Page Content added successfully', 'success')
            return redirect(url_for('dashboard_bp.update_home_page'))
        except Exception as e:
            # If something goes wrong, roll back and print the error
            db.session.rollback()
            flash(f'Error: {str(e)}', 'danger')
    else:
        # Log if form validation fails
        print("Form validation failed. Errors:", form.errors)
        flash('Please correct the errors in the form', 'danger')

    return render_template('dashboard/add-home-content.html', form=form)



@dashboard_bp.route('/update-Home-Page', methods=['GET', 'POST'])
@roles_required('Admin')
def update_home_page():
    """
    This function updates the home page content
    """
    # Retrieve the first item from the Home table
    home_content_to_update = Home.query.first()
    if not home_content_to_update:
        flash("No home content found to update, Please add the content below.", 'warning')
        return redirect(url_for('dashboard_bp.add_home_content'))

    form = HomePageContentForm()

    # Pre-populate the form with existing data for GET requests
    if request.method == 'GET':
        form.subheading.data = home_content_to_update.subheading
        form.description.data = home_content_to_update.description
        form.img_url.data = home_content_to_update.img_url

    if form.validate_on_submit():
        # Assign updated values to the home_content_to_update instance
        home_content_to_update.subheading = form.subheading.data
        home_content_to_update.description = form.description.data
        home_content_to_update.img_url = form.img_url.data

        db.session.commit()
        flash('Home Page Content updated successfully.', 'success')
        return redirect(url_for('dashboard_bp.update_home_page'))

    return render_template('dashboard/update-home-content.html', form=form, home=home_content_to_update)



# ----------------- Experience----------------- #

@dashboard_bp.route('/add-experience', methods=['GET', 'POST'])
@roles_required('Admin')
def add_experience():
    """
    This function adds a experience to the database
    :return:
    """
    form = ExperienceForm()
    if form.validate_on_submit():
        new_experience = Experience(
            duration=form.duration.data,
            role=form.role.data,
            company=form.company.data,
            location=form.location.data,
            description=form.description.data
        )
        db.session.add(new_experience)
        db.session.commit()
        flash('Experience added successfully', 'success')
        return redirect(url_for('dashboard_bp.get_experience'))
    return render_template('dashboard/add-experience.html', form=form)


@dashboard_bp.route('/work-experience', methods=['GET', 'POST'])
@roles_required('Admin')
def get_experience():
    """
    This function gets all the experience from the database
    :return:
    """
    work_experience = Experience.query.all()
    return render_template('/dashboard/experience.html', work_experience=work_experience)

@dashboard_bp.route('/delete-experience/<int:experience_id>', methods=['GET', 'DELETE'])
@roles_required('Admin')
def delete_experience(experience_id):
    """
    This function deletes a experience from the database
    :param experience_id:
    :return:
    """
    experience_to_delete = Experience.query.get_or_404(experience_id)
    db.session.delete(experience_to_delete)
    db.session.commit()
    flash('Experience deleted successfully', 'info')
    return redirect(url_for('dashboard_bp.get_experience'))

@dashboard_bp.route('/update-experience/<int:experience_id>', methods=['GET', 'POST'])
@roles_required('Admin')
def update_experience(experience_id):
    """
    This function updates the resume page content
    """
    experience_to_update = Experience.query.get_or_404(experience_id)
    form = ExperienceForm()
    if form.validate_on_submit():
        if form.duration.data:
            experience_to_update.duration = form.duration.data
        if form.role.data:
            experience_to_update.role = form.role.data
        if form.company.data:
            experience_to_update.company = form.company.data
        if form.location.data:
            experience_to_update.location = form.location.data
        if form.description.data:
            experience_to_update.description = form.description.data
        db.session.commit()
        flash('Updated successfully.', 'success')
        return redirect(url_for('dashboard_bp.get_experience'))
    return render_template('dashboard/update-experience.html', form=form, experience=experience_to_update)


# ----------------- Education----------------- #

@dashboard_bp.route('/add-education', methods=['GET', 'POST'])
@roles_required('Admin')
def add_education():
    """
    This function adds a education to the database
    :return:
    """
    form = EducationForm()
    if form.validate_on_submit():
        new_education = Education(
            duration=form.duration.data,
            institution=form.institution.data,
            qualification=form.qualification.data,
            description=form.description.data
        )
        db.session.add(new_education)
        db.session.commit()
        flash('Education added successfully', 'success')
        return redirect(url_for('dashboard_bp.get_education'))
    return render_template('dashboard/add-education.html', form=form)


@dashboard_bp.route('/education', methods=['GET', 'POST'])
@roles_required('Admin')
def get_education():
    """
    This function gets all the education from the database
    :return:
    """
    education = Education.query.all()
    return render_template('/dashboard/education.html', education_list=education)

@dashboard_bp.route('/delete-education/<int:education_id>', methods=['GET', 'DELETE'])
@roles_required('Admin')
def delete_education(education_id):
    """
    This function deletes a education from the database
    :param education_id:
    :return:
    """
    education_to_delete = Education.query.get_or_404(education_id)
    db.session.delete(education_to_delete)
    db.session.commit()
    flash('Education deleted successfully', 'info')
    return redirect(url_for('dashboard_bp.get_education'))

@dashboard_bp.route('/update-education/<int:education_id>', methods=['GET', 'POST'])
@roles_required('Admin')
def update_education(education_id):
    """
    This function updates the education page content
    """
    education_to_update = Education.query.get_or_404(education_id)
    form = EducationForm()
    if form.validate_on_submit():
        if form.duration.data:
            education_to_update.duration = form.duration.data
        if form.institution.data:
            education_to_update.institution = form.institution.data
        if form.qualification.data:
            education_to_update.qualification = form.qualification.data
        if form.description.data:
            education_to_update.description = form.description.data
        db.session.commit()
        flash('Updated successfully.', 'success')
        return redirect(url_for('dashboard_bp.get_education'))
    return render_template('dashboard/update-education.html', form=form, education=education_to_update)


# ----------------- Skills----------------- #

@dashboard_bp.route('/add-skill', methods=['GET', 'POST'])
@roles_required('Admin')
def add_skill():
    """
    This function adds a skill to the database
    :return:
    """
    form = SkillsForm()
    if form.validate_on_submit():
        new_skill = Skills(
            name=form.name.data
        )
        db.session.add(new_skill)
        db.session.commit()
        flash('Skill added successfully', 'success')
        return redirect(url_for('dashboard_bp.get_skills'))
    return render_template('dashboard/add-skill.html', form=form)

@dashboard_bp.route('/skills', methods=['GET', 'POST'])
@roles_required('Admin')
def get_skills():
    """
    This function gets all the skills from the database
    :return:
    """
    skills = Skills.query.all()
    return render_template('/dashboard/skills.html', skills=skills)

@dashboard_bp.route('/delete-skill/<int:skill_id>', methods=['GET', 'DELETE'])
@roles_required('Admin')
def delete_skill(skill_id):
    """
    This function deletes a skill from the database
    :param skill_id:
    :return:
    """
    skill_to_delete = Skills.query.get_or_404(skill_id)
    db.session.delete(skill_to_delete)
    db.session.commit()
    flash('Skill deleted successfully', 'info')
    return redirect(url_for('dashboard_bp.get_skills'))

@dashboard_bp.route('/update-skill/<int:skill_id>', methods=['GET', 'POST'])
@roles_required('Admin')
def update_skill(skill_id):
    """
    This function updates the skill page content
    """
    skill_to_update = Skills.query.get_or_404(skill_id)
    form = SkillsForm()
    if form.validate_on_submit():
        if form.name.data:
            skill_to_update.name = form.name.data
        db.session.commit()
        flash('Updated successfully.', 'success')
        return redirect(url_for('dashboard_bp.get_skills'))

    return render_template('dashboard/update-skill.html', form=form, skill=skill_to_update)


# ----------------- Language----------------- #

@dashboard_bp.route('/add-language', methods=['GET', 'POST'])
@roles_required('Admin')
def add_language():
    """
    This function adds a language to the database
    :return:
    """
    form = LanguageForm()
    if form.validate_on_submit():
        new_language = Language(
            name=form.name.data
        )
        db.session.add(new_language)
        db.session.commit()
        flash('Language added successfully', 'success')
        return redirect(url_for('dashboard_bp.get_languages'))
    return render_template('dashboard/add-language.html', form=form)


@dashboard_bp.route('/languages', methods=['GET', 'POST'])
@roles_required('Admin')
def get_languages():
    """
    This function gets all the languages from the database
    :return:
    """
    languages = Language.query.all()
    return render_template('/dashboard/languages.html', languages=languages)

@dashboard_bp.route('/delete-language/<int:language_id>', methods=['GET', 'DELETE'])
@roles_required('Admin')
def delete_language(language_id):
    """
    This function deletes a language from the database
    :param language_id:
    :return:
    """
    language_to_delete = Language.query.get_or_404(language_id)
    db.session.delete(language_to_delete)
    db.session.commit()
    flash('Language deleted successfully', 'info')
    return redirect(url_for('dashboard_bp.get_languages'))


@dashboard_bp.route('/update-language/<int:language_id>', methods=['GET', 'POST'])
@roles_required('Admin')
def update_language(language_id):
    """
    This function updates the language page content
    """
    language_to_update = Language.query.get_or_404(language_id)
    form = LanguageForm()
    if form.validate_on_submit():
        if form.name.data:
            language_to_update.name = form.name.data
        db.session.commit()
        flash('Updated successfully.', 'success')
        return redirect(url_for('dashboard_bp.get_languages'))

    return render_template('dashboard/update-language.html', form=form, language=language_to_update)


# ----------------- Projects----------------- #

@dashboard_bp.route('/add-project', methods=['GET', 'POST'])
@roles_required('Admin')
def add_project():
    """
    This function adds a project to the database
    :return:
    """
    form = ProjectsPageForm()
    if form.validate_on_submit():
        new_project = Projects(
            thumbnail=form.thumbnail.data,
            title=form.title.data,
            description=form.description.data,
            repo_link = form.repo_link.data,
            demo_link = form.demo_link.data
        )
        db.session.add(new_project)
        db.session.commit()
        flash('Project added successfully', 'success')
        return redirect(url_for('dashboard_bp.get_projects'))
    return render_template('dashboard/add-project.html', form=form)


@dashboard_bp.route('/update-project/<int:project_id>', methods=['GET', 'POST'])
@roles_required('Admin')
def update_project(project_id):
    """
    This function updates the project page content
    """
    project_to_update = Projects.query.get_or_404(project_id)
    form = ProjectsPageForm()
    if form.validate_on_submit():
        if form.thumbnail.data:
            project_to_update.thumbnail = form.thumbnail.data
        if form.title.data:
            project_to_update.title = form.title.data
        if form.description.data:
            project_to_update.description = form.description.data
        db.session.commit()

        if form.repo_link.data:
            project_to_update.repo_link = form.repo_link.data

        if form.demo_link.data:
            project_to_update.demo_link = form.demo_link.data

        flash('Updated successfully.', 'success')
        return redirect(url_for('dashboard_bp.get_projects'))

    return render_template('dashboard/update-project.html', form=form, project=project_to_update)

@dashboard_bp.route('/projects', methods=['GET', 'POST'])
@roles_required('Admin')
def get_projects():
    """
    This function gets all the projects from the database
    :return:
    """
    projects = Projects.query.all()
    return render_template('/dashboard/projects.html', projects=projects)

@dashboard_bp.route('/delete-project/<int:project_id>', methods=['GET', 'DELETE'])
@roles_required('Admin')
def delete_project(project_id):
    """
    This function deletes a project from the database
    :param project_id:
    :return:
    """
    project_to_delete = Projects.query.get_or_404(project_id)
    db.session.delete(project_to_delete)
    db.session.commit()
    flash('Project deleted successfully', 'info')
    return redirect(url_for('dashboard_bp.get_projects'))






# ---------Profile Page Content------------ #



@dashboard_bp.route('/update-education', methods=['GET', 'POST'])
@roles_required('Admin')
def update_education_page():
    """
    This function updates the education page content
    """
    form = EducationForm()
    if form.validate_on_submit():
        if form.institution.data:
            current_user.institution = form.institution.data
        if form.qualification.data:
            current_user.qualification = form.qualification.data
        if form.description.data:
            current_user.description = form.description.data
        if form.duration.data:
            current_user.duration = form.duration.data
        db.session.commit()
        flash('Education Page Content updated successfully.', 'success')
        return redirect(url_for('dashboard_bp.update_education_page'))
    return render_template('dashboard/update-education-content.html', form=form)









@dashboard_bp.route("/dashboard", methods=['POST', 'GET'])
@roles_required('Admin')
@nocache
def profile():
    email_form = UpdateEmailForm()
    phone_form = UpdatePhoneForm()
    password_form = ChangePasswordForm()
    socials_form = SocialMediaInfoForm()


    email_form.email.data = current_user.email
    phone_form.phone_number.data = current_user.phone_number


    return render_template('dashboard/profile.html', email_form=email_form, phone_form=phone_form,
                           password_form=password_form, socials_form=socials_form, about_me_form=AboutMeForm())


@dashboard_bp.route('/about-me', methods=['GET', 'POST'])
@roles_required( 'Admin')
@login_required
def about_me_form():
    """
    This function handles the about me page for the dashboard, admin, and contributor.
    """
    form = AboutMeForm()


    if form.validate_on_submit():
        about = form.about.data
        current_user.about = about
        db.session.commit()
        flash('About Me updated successfully.', 'success')
        # Redirect back to profile after successful update

    elif form.is_submitted() and not form.validate():
        for field, errors in form.errors.items():
            for error in errors:
                flash(f"{getattr(form, field).label.text}: {error}", 'danger')

    return redirect(url_for('dashboard_bp.profile'))


@dashboard_bp.route('/update-social-media', methods=['POST'])
@roles_required('Admin')
def update_social_media_form():
    form = SocialMediaInfoForm()
    if form.validate_on_submit():
        if form.github.data:
            current_user.github_url = form.github.data
        if form.linkedin.data:
            current_user.linkedin_url = form.linkedin.data
        if form.facebook.data:
            current_user.facebook_url = form.facebook.data
        if form.instagram.data:
            current_user.instagram_url = form.instagram.data
        if form.hackerrank.data:
            current_user.hackerrank_url = form.hackerrank.data
        db.session.commit()
        flash('Social media links updated successfully.', 'success')
        return redirect(url_for('dashboard_bp.profile'))
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f"{getattr(form, field).label.text}: {error}", 'danger')
    return redirect(url_for('dashboard_bp.profile'))



@dashboard_bp.route('/update-phone-number', methods=['POST'])
@roles_required('Admin')
def update_phone_number():
    form = UpdatePhoneForm()
    if form.validate_on_submit():
        phone_number = form.phone_number.data
        current_user.phone_number = phone_number
        db.session.commit()
        flash('Phone number updated successfully, refresh your browser.', 'success')
    else:
        # Handle form validation errors
        for field, errors in form.errors.items():
            for error in errors:
                flash(f"{getattr(form, field).label.text}: {error}", 'danger')
    return redirect(url_for('dashboard_bp.profile'))



@dashboard_bp.route('/update-email', methods=['POST'])
@roles_required('Admin')
def update_email():
    """
    This function updates the All dashboard's email address.
    :return:
    """
    form = UpdateEmailForm()
    if form.validate_on_submit():
        new_email = form.email.data
        current_user.email = new_email
        db.session.commit()
        flash('Email updated successfully, refresh your browser.', 'success')
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f"{getattr(form, field).label.text}: {error}", 'danger')

    return redirect(url_for('dashboard_bp.profile'))



@dashboard_bp.route('/change-password', methods=['POST'])
@roles_required('Admin')
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        current_password = form.current_password.data
        new_password = form.new_password.data

        if not check_password_hash(current_user.password, current_password):
            flash('Current password is incorrect.', 'danger')
            return redirect(url_for('dashboard_bp.profile'))

        # Update the dashboard's password
        current_user.password = generate_password_hash(new_password)
        db.session.commit()
        flash('Your password has been updated.', 'success')
    else:
        # Handle form validation errors
        for field, errors in form.errors.items():
            for error in errors:
                flash(f"{getattr(form, field).label.text}: {error}", 'danger')
    return redirect(url_for('dashboard_bp.profile'))

