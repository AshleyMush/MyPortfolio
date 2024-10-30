
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
    subheading: Mapped[str] = mapped_column(String(2000), nullable=False)
    description: Mapped[str] = mapped_column(String(2000), nullable=True)
    img_url: Mapped[str] = mapped_column(String(2000), nullable=True)




    def __repr__(self):
        return f'<HomePage{self.name}>'

    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}

class Experience(db.Model):
    __tablename__ = 'Experience'
    id: Mapped[int] = mapped_column(primary_key=True)
    duration: Mapped[str] = mapped_column(String(5000))
    role: Mapped[str] = mapped_column(String(2000))
    company: Mapped[str] = mapped_column(String(2000))
    location: Mapped[str] = mapped_column(String(2000))
    description: Mapped[str] = mapped_column(String(2000))

    def __repr__(self):
        return f'<Experience{self.title}>'

    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}

class Education(db.Model):
    __tablename__ = 'Education'
    id: Mapped[int] = mapped_column(primary_key=True)
    duration: Mapped[str] = mapped_column(String(500))
    institution: Mapped[str] = mapped_column(String(2000))
    qualification: Mapped[str] = mapped_column(String(2000))
    description: Mapped[str] = mapped_column(String(2000))

    def __repr__(self):
        return f'<Education{self.title}>'

    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}

class Language(db.Model):
    __tablename__ = 'Languages'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(2000), nullable=False)

    def __repr__(self):
        return f'<Language{self.name}>'

    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}

class Skills(db.Model):
    __tablename__ = 'Skills'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(2000), nullable=False)

    def __repr__(self):
        return f'<Skills{self.name}>'

    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}


class Projects(db.Model):
    __tablename__ = 'Projects'
    id: Mapped[int] = mapped_column(primary_key=True)
    thumbnail: Mapped[str] = mapped_column(String(2000), nullable=True)
    title: Mapped[str] = mapped_column(String(2000), nullable=True)
    description: Mapped[str] = mapped_column(String(2000), nullable=True)
    repo_link: Mapped[str] = mapped_column(String(2000), nullable=True)
    demo_link: Mapped[str] = mapped_column(String(2000), nullable=True)


    def __repr__(self):
        return f'<Projects {self.title}>'

    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}
