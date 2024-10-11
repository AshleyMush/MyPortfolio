from flask import Blueprint

user_bp = Blueprint(
    'user_bp',
    __name__,
    template_folder='templates',
    static_folder='static',

)

from . import routes  # Import routes after creating the blueprint