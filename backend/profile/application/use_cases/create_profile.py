from profile.domain.entities import Profile

from account.application.interfaces.uow import UnitOfWork


def create_profile(
    uow: UnitOfWork,
    user_id: int,
) -> Profile:
    with uow:
        existing_profile = uow.profiles.get_by_user_id(user_id)
        if existing_profile is not None:
            return existing_profile

        profile = Profile(user_id=user_id)
        profile = uow.profiles.save(profile)

        uow.commit()

        return profile
