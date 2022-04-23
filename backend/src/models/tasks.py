import sqlalchemy as sa
from ..core.database import db
from datetime import datetime


class Task(db.Model):
    id = sa.Column(sa.Integer, primary_key=True, index=True)
    title = sa.Column(sa.String(length=255))
    description = sa.Column(sa.Text)
    created_at = sa.Column(sa.DateTime, nullable=False, default=datetime.utcnow)
    deadline = sa.Column(sa.DateTime, nullable=True)
    # user_id
