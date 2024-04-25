from pydantic import Field, BaseModel
from datetime import datetime, timezone
from uuid import UUID, uuid4


class BaseMixin(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
