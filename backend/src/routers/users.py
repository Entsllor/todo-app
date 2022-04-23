from flask import Blueprint, abort
from flask_pydantic import validate
from sqlalchemy.exc import IntegrityError

from src.core.database import db
from src.schemas.users import UserCreate, UserOut
from src import models
from src.utils.passwords import get_password_hash

blueprint = Blueprint('users', __name__)


@blueprint.post("/sign-up")
@validate(on_success_status=201)
def create_user(body: UserCreate):
    hashed_password = get_password_hash(body.password)
    db_user = models.User(**body.dict(exclude={'password'}), hashed_password=hashed_password)
    db.session.add(db_user)
    try:
        db.session.flush()
    except IntegrityError:
        abort(400)
    db.session.commit()
    db.session.refresh(db_user)
    return UserOut.from_orm(db_user)
