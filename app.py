from flask import Flask, render_template
from flask_bootstrap import Bootstrap5
from flask_login import LoginManager
from flask_ckeditor import CKEditor
from flask_wtf.csrf import CSRFProtect
from models import db
from models.user import User
from controllers.user import user_bp
from controllers.auth import auth_bp
from controllers.portfolio import portfolio_bp
import os
from sqlalchemy.exc import SQLAlchemyError
from flask_migrate import Migrate


# Initialize Flask application
app = Flask(__name__)
BASEDIR = os.path.abspath(os.path.dirname(__file__))
app.config['SECRET_KEY'] = os.environ.get("SECRET_APP_KEY", "default_secret_key")
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(BASEDIR, 'Portfolio.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
ckeditor = CKEditor(app)
Bootstrap5(app)
csrf = CSRFProtect(app)
db.init_app(app)


# # Initialize Flask-Migrate
migrate = Migrate(app, db)


# --- Initialize Flask-Login ---
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth_bp.login'  # Redirect to login if not authenticated

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, user_id)

# ------- Register the Blueprints --------
app.register_blueprint(user_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(portfolio_bp)


    # ------- Error Handlers --------

@app.errorhandler(404)
def page_not_found(e):
    return render_template('dashboard/404.html'), 404

# ------- Create the Database --------
with app.app_context():
    try:
        print("Attempting to create tables...")
        db.create_all()
        print("Database and tables created successfully.")
    except SQLAlchemyError as e:
        print(f"Error occurred during db.create_all(): {e}")
        db.session.rollback()
    except Exception as e:
        print(f"Unexpected error: {e}")

# ------- Run the Application --------
if __name__ == "__main__":
    app.run(debug=True, port=5002)
