from __future__ import annotations

from dataclasses import replace
from profile.domain.entities import Profile
from typing import Any

from account.domain.entities import Account


class FakeAccountRepository:
    def __init__(self, accounts: list[Account] | None = None) -> None:
        self._accounts: list[Account] = list(accounts or [])
        self.saved_accounts: list[Account] = []
        self.save_result: Account | None = None
        self.next_id = max(
            (
                account.id
                for account in self._accounts
                if account.id is not None
            ),
            default=0,
        ) + 1

    def get_by_id(self, account_id: int) -> Account | None:
        return next(
            (
                account
                for account in self._accounts
                if account.id == account_id
            ),
            None,
        )

    def get_by_email(self, email: str) -> Account | None:
        return next(
            (account for account in self._accounts if account.email == email),
            None,
        )

    def get_by_username(self, username: str) -> Account | None:
        return next(
            (
                account
                for account in self._accounts
                if account.username == username
            ),
            None,
        )

    def save(self, account: Account) -> Account:
        self.saved_accounts.append(account)

        if self.save_result is not None:
            result = self.save_result
        elif account.id is None:
            result = replace(account, id=self.next_id)
            self.next_id += 1
        else:
            result = account

        self._accounts = [
            saved for saved in self._accounts if saved.id != result.id
        ]
        self._accounts.append(result)
        return result


class FakeProfileRepository:
    def __init__(self, profiles: list[Profile] | None = None) -> None:
        self._profiles: list[Profile] = list(profiles or [])
        self.saved_profiles: list[Profile] = []
        self.save_result: Profile | None = None
        self.next_id = max(
            (
                profile.id
                for profile in self._profiles
                if profile.id is not None
            ),
            default=0,
        ) + 1

    def get_by_id(self, profile_id: int) -> Profile | None:
        return next(
            (
                profile
                for profile in self._profiles
                if profile.id == profile_id
            ),
            None,
        )

    def get_by_user_id(self, user_id: int) -> Profile | None:
        return next(
            (
                profile
                for profile in self._profiles
                if profile.user_id == user_id
            ),
            None,
        )

    def save(self, save_profile: Profile) -> Profile:
        self.saved_profiles.append(save_profile)

        if self.save_result is not None:
            result = self.save_result
        elif save_profile.id is None:
            result = replace(save_profile, id=self.next_id)
            self.next_id += 1
        else:
            result = save_profile

        self._profiles = [
            profile for profile in self._profiles if profile.id != result.id
        ]
        self._profiles.append(result)
        return result


class FakeUnitOfWork:
    def __init__(
        self,
        accounts: FakeAccountRepository | None = None,
        profiles: FakeProfileRepository | None = None,
    ) -> None:
        self.accounts = accounts or FakeAccountRepository()
        self.profiles = profiles or FakeProfileRepository()
        self.enter_calls = 0
        self.exit_calls = 0
        self.commit_calls = 0
        self.rollback_calls = 0

    def __enter__(self) -> FakeUnitOfWork:
        self.enter_calls += 1
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        self.exit_calls += 1

    def commit(self) -> None:
        self.commit_calls += 1

    def rollback(self) -> None:
        self.rollback_calls += 1


class FakePasswordService:
    def __init__(self) -> None:
        self.hashed_inputs: list[str] = []
        self.checked_pairs: list[tuple[str, str]] = []
        self.valid_pairs: set[tuple[str, str]] = set()

    def hash_password(self, password: str) -> str:
        self.hashed_inputs.append(password)
        return f'hashed::{password}'

    def check_password(self, password: str, hashed_password: str) -> bool:
        self.checked_pairs.append((password, hashed_password))
        return (password, hashed_password) in self.valid_pairs


class FakeMailSender:
    def __init__(self) -> None:
        self.sent_codes: list[tuple[int, str]] = []

    def send_code(self, code: int, to_email: str) -> None:
        self.sent_codes.append((code, to_email))


class FakeCacheService:
    def __init__(self) -> None:
        self._storage: dict[str, dict[str, Any]] = {}
        self.posted_codes: list[tuple[Account, int]] = []
        self.deleted_emails: list[str] = []
        self.delete_result = True

    def post_confirmation_code(self, account: Account, code: int) -> None:
        self.posted_codes.append((account, code))
        self._storage[account.email] = {
            'code': code,
            'username': account.username,
            'password_hash': account.password_hash,
        }

    def get_info_by_email(self, email: str) -> dict[str, Any] | None:
        return self._storage.get(email)

    def delete_by_email(self, email: str) -> bool:
        self.deleted_emails.append(email)
        self._storage.pop(email, None)
        return self.delete_result

    def seed(self, email: str, info: dict[str, Any]) -> None:
        self._storage[email] = info


class FakeAuthService:
    def __init__(self) -> None:
        self.created_for_ids: list[int] = []
        self.token_pair: dict[str, str | int] = {
            'access_token': 'access',
            'refresh_token': 'refresh',
            'token_type': 'bearer',
            'expires_in': 3600,
        }
        self.payload: dict[str, str] = {'sub': '1'}
        self.seen_tokens: list[str] = []

    def create_token_pair(self, account_id: int) -> dict[str, str | int]:
        self.created_for_ids.append(account_id)
        return self.token_pair

    def refresh_token_pair(self, refresh_token: str) -> dict[str, str | int]:
        return self.token_pair

    def get_payload(self, access_token: str) -> dict[str, str]:
        self.seen_tokens.append(access_token)
        return self.payload
