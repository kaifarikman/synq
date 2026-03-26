from sqlalchemy import select

from app.db import Session
from profile.domain.entities import Profile
from profile.infrastructure.persistence.mappers import ProfileMapper
from profile.infrastructure.persistence.models import ProfileModel


class SQLAlchemyProfileRepository:
    def get_by_id(self, profile_id: int) -> Profile | None:
        with Session() as session:
            profile = session.get(ProfileModel, profile_id)
            return ProfileMapper.to_domain(profile) if profile else None

    def get_by_user_id(self, user_id: int) -> Profile | None:
        with Session() as session:
            query = select(ProfileModel).where(ProfileModel.user_id == user_id)
            profile = session.scalar(query)
            return ProfileMapper.to_domain(profile) if profile else None

    def save(self, save_profile: Profile) -> Profile:
        with Session() as session:
            if save_profile.id is not None:
                model = session.get(ProfileModel, save_profile.id)
            else:
                model = None

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
                session.add(model)

            session.commit()
            session.refresh(model)
            return ProfileMapper.to_domain(model)
