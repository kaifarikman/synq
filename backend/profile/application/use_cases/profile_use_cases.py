from profile.application.read_models import ProfileReadModel
from profile.domain.ports import ProfileRepository

from .get_my_profile import get_my_profile
from .update_my_profile import update_my_profile


class ProfileUseCases:
    def __init__(
        self,
        profile_repository: ProfileRepository,
    ):
        self.profile_repository = profile_repository

    def get_my_profile(self, user_id: int) -> ProfileReadModel:
        return get_my_profile(
            profile_repository=self.profile_repository,
            user_id=user_id,
        )

    def update_my_profile(
        self,
        user_id: int,
        full_name: str | None,
        bio: str | None,
    ) -> ProfileReadModel:
        return update_my_profile(
            profile_repository=self.profile_repository,
            user_id=user_id,
            full_name=full_name,
            bio=bio,
        )
