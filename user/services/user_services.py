from models import db
from user.models import User
from user.schemas.UserSchema import user_schema


def get_user_by_email(email: str):
    user = User.query.filter_by(email=email).first()

    return user_schema.dump(user) if user else None
