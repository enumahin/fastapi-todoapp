from core.auth.user.user_model import User
from sqlalchemy import or_


def add_user(user: User, db):
    try:
        db.add(user)
        db.commit()
        return user
    except Exception as ex:
        db.rollback()
        return ex


def get_user(user_id: int, db):
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_email(email, db):
    return db.query(User).filter(User.email == email).first()


def get_user_by_email_or_username(email, db):
    return db.query(User).filter(or_(User.email == email, User.username == email)).first()