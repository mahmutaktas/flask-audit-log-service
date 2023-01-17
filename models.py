from sqlalchemy.ext.declarative import declared_attr
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Base(db.Model):

    __abstract__ = True

    @declared_attr
    def created_by(cls):
        return db.Column(db.Integer, db.ForeignKey('users.id'))

    @declared_attr
    def created_date(cls):
        return db.Column(db.DateTime, default=db.func.current_timestamp())

    @declared_attr
    def updated_by(cls):
        return db.Column(db.Integer, db.ForeignKey('users.id'))

    @declared_attr
    def updated_date(cls):
        return db.Column(db.DateTime, onupdate=db.func.current_timestamp())
