from profile.domain.entities import Profile
from profile.domain.ports import ProfileRepository


def create_profile(
    profile_repository: ProfileRepository,
    user_id: int,
) -> Profile:
    existing_profile = profile_repository.get_by_user_id(user_id)
    if existing_profile is not None:
        return existing_profile

    profile = Profile(user_id=user_id)
    return profile_repository.save(profile)
