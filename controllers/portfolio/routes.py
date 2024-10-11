from . import portfolio_bp









@portfolio_bp.route('/home')
def home():
    return 'Portfolio Home Page'
    # return render_template('portfolio/home.html')