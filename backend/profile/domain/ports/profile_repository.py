from profile.domain.entities import Profile
from typing import Protocol


class ProfileRepository(Protocol):
    def get_by_id(self, profile_id: int) -> Profile | None: ...

    def get_by_user_id(self, user_id: int) -> Profile | None: ...

    def save(self, save_profile: Profile) -> Profile: ...
