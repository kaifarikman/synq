from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Optional
from uuid import UUID, uuid4


@dataclass
class Profile:
    user_id: int

    id: Optional[int] = field(default=None)
    uuid: UUID = field(default_factory=uuid4)

    full_name: Optional[str] = field(default=None)
    bio: Optional[str] = field(default=None)

    created_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
    updated_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc),
    )
