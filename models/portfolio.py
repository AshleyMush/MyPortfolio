
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey, Table
from sqlalchemy.orm import relationship
from sqlalchemy import String, Integer, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from flask_login import UserMixin

from . import db



class Home(db.Model):
    __tablename__ = 'HomePage'
    id: Mapped[int] = mapped_column(primary_key=True)
    subheading: Mapped[str] = mapped_column(String(500), nullable=False)  # Increased from 255 to 500
    description: Mapped[str] = mapped_column(String(1000), nullable=True)  # Increased from 255 to 1000
    img_url: Mapped[str] = mapped_column(String(500), nullable=True)  # Increased from 255 to 500

    def __repr__(self):
        return f'<HomePage{self.name}>'

    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}

class Experience(db.Model):
    __tablename__ = 'Experience'
    id: Mapped[int] = mapped_column(primary_key=True)
    duration: Mapped[str] = mapped_column(String(100))  # Increased from 50 to 100
    role: Mapped[str] = mapped_column(String(200))  # Increased from 100 to 200
    company: Mapped[str] = mapped_column(String(200))  # Increased from 100 to 200
    location: Mapped[str] = mapped_column(String(200))  # Increased from 100 to 200
    description: Mapped[str] = mapped_column(String(1000))  # Increased from 255 to 1000

    def __repr__(self):
        return f'<Experience{self.title}>'

    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}

class Education(db.Model):
    __tablename__ = 'Education'
    id: Mapped[int] = mapped_column(primary_key=True)
    duration: Mapped[str] = mapped_column(String(100))  # Increased from 50 to 100
    institution: Mapped[str] = mapped_column(String(200))  # Increased from 100 to 200
    qualification: Mapped[str] = mapped_column(String(200))  # Increased from 100 to 200
    description: Mapped[str] = mapped_column(String(1000))  # Increased from 255 to 1000

    def __repr__(self):
        return f'<Education{self.title}>'

    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}

class Language(db.Model):
    __tablename__ = 'Languages'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(150), nullable=False)  # Increased from 100 to 150

    def __repr__(self):
        return f'<Language{self.name}>'

    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}

class Skills(db.Model):
    __tablename__ = 'Skills'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(150), nullable=False)  # Increased from 100 to 150

    def __repr__(self):
        return f'<Skills{self.name}>'

    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}


class Projects(db.Model):
    __tablename__ = 'Projects'
    id: Mapped[int] = mapped_column(primary_key=True)
    thumbnail: Mapped[str] = mapped_column(String(500), nullable=True)  # Increased from 255 to 500
    title: Mapped[str] = mapped_column(String(200), nullable=True)  # Increased from 100 to 200
    description: Mapped[str] = mapped_column(String(1000), nullable=True)  # Increased from 255 to 1000
    repo_link: Mapped[str] = mapped_column(String(500), nullable=True)  # Increased from 255 to 500
    demo_link: Mapped[str] = mapped_column(String(500), nullable=True)  # Increased from 255 to 500

    def __repr__(self):
        return f'<Projects {self.title}>'

    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}
