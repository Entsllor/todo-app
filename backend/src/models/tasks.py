import enum
import uuid

import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID
from ..core.database import db
from datetime import datetime


class TaskStatusEnum(enum.Enum):
    PENDING = "pending"
    COMPLETED = "completed"


class Task(db.Model):
    id = sa.Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    title = sa.Column(sa.String(length=255))
    description = sa.Column(sa.Text, nullable=True)
    created_at = sa.Column(sa.DateTime, nullable=False, default=datetime.utcnow)
    deadline = sa.Column(sa.DateTime, nullable=True)
    is_completed = sa.Column(sa.Boolean, default=False)

    @property
    def is_expired(self):
        return datetime.now() < self.deadline

    @property
    def status(self):
        return TaskStatusEnum.COMPLETED.value if self.is_completed else TaskStatusEnum.PENDING.value
