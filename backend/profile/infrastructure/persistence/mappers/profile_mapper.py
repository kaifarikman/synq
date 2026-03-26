from profile.domain.entities import Profile
from profile.infrastructure.persistence.models import ProfileModel


class ProfileMapper:
    @staticmethod
    def to_domain(model: ProfileModel) -> Profile:
        return Profile(
            user_id=model.user_id,
            id=model.id,
            uuid=model.uuid,
            full_name=model.full_name,
            bio=model.bio,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )
