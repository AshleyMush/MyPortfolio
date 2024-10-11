# Route for authentication
from forms.auth import RegisterForm, LoginForm
from flask_login import login_user, current_user, logout_user
from models.user import User, db
from flask import Blueprint, render_template, redirect, url_for, flash, current_app, session
from utils.encryption import hash_and_salt_password, check_password_hash
from utils.email_utils import send_password_reset_email

from . import auth_bp
from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired
from flask import request





# Todo: add /login route

@auth_bp.route('/login', methods=["GET", "POST"])
def login():
    """
    This function handles the login process.

    If the dashboard is already authenticated, redirect to the dashboard dashboard.
    If the form is valid on submission, check the dashboard's credentials.
    If the credentials are valid, log the dashboard in and redirect based on their role.
    If the credentials are invalid, flash an error message and render the login form again.
    """
    # Check if any users exist in the database.
    user_count = User.query.count()
    if user_count == 0:
        hide_registration = True  # First dashboard becomes Admin
    else:

        hide_registration = False

    if current_user.is_authenticated:

            return redirect(url_for('user_bp.profile'))

    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        result = db.session.execute(db.select(User).where(User.email == email))

        user = result.scalar()

        if user and check_password_hash(user.password, password):
            flash('Logged in successfully', 'success')
            login_user(user, remember=form.remember_me.data)  # Uses remember_me checkbox value

            return redirect(url_for('user_bp.profile'))

        else:
            flash('Invalid email or password', 'danger')
            return render_template("/auth/login.html", form=form)

    return render_template("/auth/login.html", form=form, hide_registration=hide_registration)





@auth_bp.route('/logout')
def logout():
    """
    This function logs out the dashboard and redirects them to the BLOG page.
    :return:
    """
    session.clear()
    logout_user()

    return redirect(url_for('portfolio_bp.home'))






@auth_bp.route('/register', methods=["GET", "POST"])
def register():

    form = RegisterForm()

    # Check if any users exist in the database.
    user_count = User.query.count()
    if user_count == 0:
        role = 'Admin'  # First dashboard becomes Admin
    else:

        flash('Registration is closed.', 'info')
        return redirect(url_for('portfolio_bp.home'))

    if form.validate_on_submit() and form.data:
        result = db.session.execute(db.select(User).where(User.email == form.email.data))
        user = result.scalar()
        if user:
            flash('Email already exists, Login instead', 'danger')
            return redirect(url_for('auth_bp.login'))

        # Hash the password with salt
        hashed_password = hash_and_salt_password(form.password.data)
        # Create new dashboard
        new_user = User(
            email=form.email.data,
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            password=hashed_password,  # Use the hashed password string
            role=role
        )

        # Add and commit the dashboard to the database
        db.session.add(new_user)
        flash('Registered successfully', 'success')
        db.session.commit()
        # Log in the dashboard
        login_user(new_user)
        if new_user.role == "Admin":
            return redirect(url_for('user_bp.profile'))
        else:

            return redirect(url_for("user_bp.profile"))

    else:
        if form.errors:
            for field, errors in form.errors.items():
                for error in errors:
                    flash(f'Error in {field}: {error}', 'danger')

    return render_template("/auth/register.html", form=form)

@auth_bp.route('/forgot-password', methods=["GET", "POST"])
def forgot_password():
    if request.method == 'POST':
        email = request.form.get('email')
        user = User.query.filter_by(email=email).first()
        if user:
            send_password_reset_email(user.email)
            flash('A password reset email has been sent to your email address.', 'info')
            return redirect(url_for('auth_bp.login'))
        else:
            flash('Email address not found.', 'danger')
            return redirect(url_for('auth_bp.forgot_password'))
    return render_template("/auth/forgot-password.html")

@auth_bp.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    s = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    try:
        email = s.loads(token, salt='password-reset-salt', max_age=3600)  # Token expires after 1 hour
    except SignatureExpired:
        flash('The password reset link has expired.', 'danger')
        return redirect(url_for('auth_bp.forgot_password'))
    except BadSignature:
        flash('Invalid password reset link.', 'danger')
        return redirect(url_for('auth_bp.forgot_password'))

    if request.method == 'POST':
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        if password != confirm_password:
            flash('Passwords do not match.', 'danger')
            return redirect(url_for('auth_bp.reset_password', token=token))
        if len(password) < 8:
            flash('Password must be at least 8 characters long.', 'danger')
            return redirect(url_for('auth_bp.reset_password', token=token))
        # Update the dashboard's password
        user = User.query.filter_by(email=email).first()
        if user:
            user.password = hash_and_salt_password(password)
            db.session.commit()
            flash('Your password has been updated!', 'success')
            return redirect(url_for('auth_bp.login'))
        else:
            flash('User not found.', 'danger')
            return redirect(url_for('auth_bp.register'))
    return render_template('/auth/reset-password.html', token=token)
