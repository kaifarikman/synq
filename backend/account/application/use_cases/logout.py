from account.application.interfaces.auth_service import AuthService


def logout(auth_service: AuthService, access_token: str) -> None:
    auth_service.get_payload(access_token)
