from typing import Protocol

from profile.domain.entities import Profile


class ProfileRepository(Protocol):
    def get_by_id(self, id: int) -> Profile | None: ...

    def get_by_user_id(self, user_id: int) -> Profile | None: ...

    def save(self, profile: Profile) -> Profile: ...
