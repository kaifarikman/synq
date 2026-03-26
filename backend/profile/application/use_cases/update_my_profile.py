from profile.application.exceptions import ProfileNotFound
from profile.application.read_models import ProfileReadModel

from account.application.interfaces.uow import UnitOfWork


def update_my_profile(
    uow: UnitOfWork,
    user_id: int,
    full_name: str | None,
    bio: str | None,
) -> ProfileReadModel:
    with uow:
        profile = uow.profiles.get_by_user_id(user_id)
        if profile is None:
            raise ProfileNotFound('Профиль не найден')

        profile.full_name = full_name
        profile.bio = bio
        profile = uow.profiles.save(profile)

        if profile.id is None:
            raise ProfileNotFound('Профиль не найден')

        uow.commit()

        return ProfileReadModel(
            id=profile.id,
            user_id=profile.user_id,
            uuid=profile.uuid,
            full_name=profile.full_name,
            bio=profile.bio,
        )
