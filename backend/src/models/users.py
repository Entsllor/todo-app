from datetime import datetime

from src.core.database import db
import sqlalchemy as sa
import uuid
from sqlalchemy.dialects.postgresql import UUID


class User(db.Model):
    id = sa.Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    login = sa.Column(sa.String(length=255), index=True, unique=True)
    created_at = sa.Column(sa.DateTime, default=datetime.utcnow)
    hashed_password = sa.Column(sa.String(length=255))
