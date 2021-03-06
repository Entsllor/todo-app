import enum
import uuid
from datetime import datetime

import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from ..core.database import db


class TaskStatusEnum(enum.Enum):
    PENDING = "pending"
    COMPLETED = "completed"


class Task(db.Model):
    id = sa.Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    title = sa.Column(sa.String(length=255))
    description = sa.Column(sa.Text, nullable=True)
    created_at = sa.Column(sa.DateTime, nullable=False, default=datetime.utcnow)
    deadline = sa.Column(sa.DateTime, nullable=True)
    is_completed = sa.Column(sa.Boolean, default=False, nullable=False)
    user_id = sa.Column(UUID(as_uuid=True), sa.ForeignKey("user.id"), nullable=False)
    user = relationship("User", backref="tasks")

    @property
    def is_expired(self):
        return datetime.now() < self.deadline

    @property
    def status(self):
        return TaskStatusEnum.COMPLETED.value if self.is_completed else TaskStatusEnum.PENDING.value
