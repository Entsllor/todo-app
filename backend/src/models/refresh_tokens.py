import time

import secrets
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from ..core.database import db


class RefreshToken(db.Model):
    __tablename__ = "refresh_token"
    body = sa.Column(sa.String(length=127), primary_key=True, default=lambda: secrets.token_urlsafe(90))
    user_id = sa.Column(UUID(as_uuid=True), sa.ForeignKey("user.id"))
    user = relationship("User", backref="refresh_tokens")
    expire_at = sa.Column(sa.Integer, index=True)  # Unix time

    @property
    def is_active(self):
        return time.time() < self.expire_at
