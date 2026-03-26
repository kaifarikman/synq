from dataclasses import dataclass


@dataclass(frozen=True)
class CurrentUserReadModel:
    id: int
    email: str
    username: str
