from datetime import timezone
from profile.application.exceptions import ProfileNotFound
from profile.application.use_cases.create_profile import create_profile
from profile.application.use_cases.get_my_profile import get_my_profile
from profile.application.use_cases.update_my_profile import update_my_profile
from profile.domain.entities import Profile
from unittest import TestCase

from tests.fakes import FakeProfileRepository, FakeUnitOfWork


class CreateProfileTests(TestCase):
    def test_create_profile_returns_existing_profile(self) -> None:
        existing_profile = Profile(id=5, user_id=10)
        uow = FakeUnitOfWork(
            profiles=FakeProfileRepository(profiles=[existing_profile]),
        )

        result = create_profile(uow=uow, user_id=10)

        self.assertIs(result, existing_profile)
        self.assertEqual(uow.commit_calls, 0)

    def test_create_profile_saves_new_profile(self) -> None:
        uow = FakeUnitOfWork()

        result = create_profile(uow=uow, user_id=10)

        self.assertEqual(result.user_id, 10)
        self.assertEqual(result.id, 1)
        self.assertEqual(uow.commit_calls, 1)
        self.assertEqual(len(uow.profiles.saved_profiles), 1)


class GetMyProfileTests(TestCase):
    def test_get_my_profile_raises_when_profile_missing(self) -> None:
        with self.assertRaises(ProfileNotFound):
            get_my_profile(uow=FakeUnitOfWork(), user_id=10)

    def test_get_my_profile_returns_read_model(self) -> None:
        profile = Profile(id=5, user_id=10, full_name='Kai', bio='Bio')
        uow = FakeUnitOfWork(
            profiles=FakeProfileRepository(profiles=[profile]),
        )

        result = get_my_profile(uow=uow, user_id=10)

        self.assertEqual(result.id, 5)
        self.assertEqual(result.user_id, 10)
        self.assertEqual(result.full_name, 'Kai')
        self.assertEqual(result.bio, 'Bio')


class UpdateMyProfileTests(TestCase):
    def test_update_my_profile_raises_when_profile_missing(self) -> None:
        with self.assertRaises(ProfileNotFound):
            update_my_profile(
                uow=FakeUnitOfWork(),
                user_id=10,
                full_name='Kai',
                bio='Bio',
            )

    def test_update_my_profile_raises_when_saved_profile_has_no_id(
        self,
    ) -> None:
        existing_profile = Profile(id=5, user_id=10)
        profiles = FakeProfileRepository(profiles=[existing_profile])
        profiles.save_result = Profile(id=None, user_id=10)
        uow = FakeUnitOfWork(profiles=profiles)

        with self.assertRaises(ProfileNotFound):
            update_my_profile(
                uow=uow,
                user_id=10,
                full_name='Kai',
                bio='Bio',
            )

    def test_update_my_profile_updates_and_returns_read_model(self) -> None:
        existing_profile = Profile(id=5, user_id=10)
        uow = FakeUnitOfWork(
            profiles=FakeProfileRepository(profiles=[existing_profile]),
        )

        result = update_my_profile(
            uow=uow,
            user_id=10,
            full_name='Kai',
            bio='Bio',
        )

        self.assertEqual(result.id, 5)
        self.assertEqual(result.user_id, 10)
        self.assertEqual(result.full_name, 'Kai')
        self.assertEqual(result.bio, 'Bio')
        self.assertEqual(uow.commit_calls, 1)


class ProfileEntityTests(TestCase):
    def test_profile_generates_uuid_and_timezone_aware_timestamps(
        self,
    ) -> None:
        profile = Profile(user_id=10)

        self.assertIsNotNone(profile.uuid)
        self.assertEqual(profile.created_at.tzinfo, timezone.utc)
        self.assertEqual(profile.updated_at.tzinfo, timezone.utc)
