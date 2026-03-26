from dataclasses import dataclass
from typing import Optional
from uuid import UUID


@dataclass(frozen=True)
class ProfileReadModel:
    id: int
    user_id: int
    uuid: UUID
    full_name: Optional[str]
    bio: Optional[str]
