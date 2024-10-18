from flask import Flask, jsonify, request
from flask_bootstrap import Bootstrap5
from flask_login import LoginManager, current_user
from config import Config
from flask_ckeditor import CKEditor
from flask_bootstrap import Bootstrap
from flask_wtf.csrf import CSRFProtect
from models import db
from models.user import User
from controllers.user import user_bp
from controllers.auth import auth_bp
from controllers.portfolio import portfolio_bp
from models.user import User
from models import db
from models.portfolio import  Experience, Projects, Skills
import os
from sqlalchemy.exc import SQLAlchemyError
from models.user import User




app = Flask(__name__)
app.config.from_object(Config)

ckeditor = CKEditor(app)
Bootstrap5(app)
csrf = CSRFProtect(app)
# -----------------Configure DB-------------------------
db.init_app(app)



# --- Initialize Flask-Login ---
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth_bp.login' # Redirect to login if not authenticated

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, user_id)



# -------register the blueprints--------
app.register_blueprint(user_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(portfolio_bp)



# # Initialize Flask-Migrate
# migrate = Migrate(app, db)


with app.app_context():
    try:
        db.create_all()
    except SQLAlchemyError as e:
        print(f"Error occurred: {e}")
        db.session.rollback()
    finally:
        db.session.close()

if __name__ == "__main__":
    app.run(debug=True, port=5002) # TODO: Remove port before deployment AND DEBUG=True