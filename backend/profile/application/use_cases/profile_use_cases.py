from profile.application.read_models import ProfileReadModel
from profile.application.use_cases.create_profile import create_profile
from profile.application.use_cases.get_my_profile import get_my_profile
from profile.application.use_cases.update_my_profile import update_my_profile
from profile.domain.entities.profile import Profile

from account.application.interfaces.uow import UnitOfWork


class ProfileUseCases:
    def __init__(self, uow: UnitOfWork) -> None:
        self.uow = uow

    def get_my_profile(self, user_id: int) -> ProfileReadModel:
        return get_my_profile(
            uow=self.uow,
            user_id=user_id,
        )

    def update_my_profile(
        self,
        user_id: int,
        full_name: str | None,
        bio: str | None,
    ) -> ProfileReadModel:
        return update_my_profile(
            uow=self.uow,
            user_id=user_id,
            full_name=full_name,
            bio=bio,
        )

    def create_profile(self, user_id: int) -> Profile:
        return create_profile(
            uow=self.uow,
            user_id=user_id,
        )
