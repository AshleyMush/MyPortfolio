# models/__init__.py

# This file is used to import all the models in the application through models.name_of_model


from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()



from .portfolio import AboutMe, Resume, Projects, Skills
from .user import User