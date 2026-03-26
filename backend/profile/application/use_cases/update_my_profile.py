from profile.application.exceptions import ProfileNotFound
from profile.application.read_models import ProfileReadModel
from profile.domain.ports import ProfileRepository


def update_my_profile(
    profile_repository: ProfileRepository,
    user_id: int,
    full_name: str | None,
    bio: str | None,
) -> ProfileReadModel:
    profile = profile_repository.get_by_user_id(user_id)
    if profile is None:
        raise ProfileNotFound('Профиль не найден')

    profile.full_name = full_name
    profile.bio = bio
    profile = profile_repository.save(profile)

    if profile.id is None:
        raise ProfileNotFound('Профиль не найден')

    return ProfileReadModel(
        id=profile.id,
        user_id=profile.user_id,
        uuid=profile.uuid,
        full_name=profile.full_name,
        bio=profile.bio,
    )
