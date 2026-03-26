from profile.domain.entities import Profile
from profile.infrastructure.persistence.mappers import ProfileMapper
from profile.infrastructure.persistence.models import ProfileModel

from sqlalchemy import select
from sqlalchemy.orm import Session


class SQLAlchemyProfileRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def get_by_id(self, profile_id: int) -> Profile | None:
        profile = self.session.get(ProfileModel, profile_id)
        return ProfileMapper.to_domain(profile) if profile else None

    def get_by_user_id(self, user_id: int) -> Profile | None:
        query = select(ProfileModel).where(ProfileModel.user_id == user_id)
        profile = self.session.scalar(query)
        return ProfileMapper.to_domain(profile) if profile else None

    def save(self, save_profile: Profile) -> Profile:
        model = (
            self.session.get(ProfileModel, save_profile.id)
            if save_profile.id is not None
            else None
        )

        if model:
            model.full_name = save_profile.full_name
            model.bio = save_profile.bio
            model.uuid = save_profile.uuid
            model.user_id = save_profile.user_id
        else:
            model = ProfileModel(
                uuid=save_profile.uuid,
                user_id=save_profile.user_id,
                full_name=save_profile.full_name,
                bio=save_profile.bio,
            )
            self.session.add(model)
            self.session.flush()

        return ProfileMapper.to_domain(model)
