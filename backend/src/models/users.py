import uuid
from datetime import datetime

import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID

from ..core.database import db
from ..utils.passwords import verify_password


class User(db.Model):
    id = sa.Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    login = sa.Column(sa.String(length=255), index=True, unique=True)
    created_at = sa.Column(sa.DateTime, default=datetime.utcnow)
    hashed_password = sa.Column(sa.String(length=255))

    def password_match(self, plain_password: str) -> bool:
        return verify_password(plain_password=plain_password, hashed_password=self.hashed_password)
