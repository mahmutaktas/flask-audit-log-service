from models import db, Base


class User(Base):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)

    email = db.Column(db.String(255), unique=True, index=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(500), nullable=True)
    surname = db.Column(db.String(500), nullable=True)
