from flask import Blueprint

portfolio_bp = Blueprint(
    'portfolio_bp',
    __name__,
    template_folder='templates',
    static_folder='static',
    url_prefix='/portfolio'
)

from . import routes