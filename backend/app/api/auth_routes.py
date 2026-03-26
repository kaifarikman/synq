"""Ручки FastAPI приложения в контексте Authentication"""

from fastapi import APIRouter, Depends, HTTPException, Response, status

from account.application.exceptions import (
    AccountAlreadyExist,
    AccountIsDeactivate,
    AccountNotFound,
    InvalidPassword,
    UsernameAlreadyExist,
)
from account.application.use_cases import AuthUseCases
from app.api.dependencies import get_auth_use_cases, get_bearer_token
from app.api.schemas import (
    AccountLoginSchema,
    AccountRegisterSchema,
    EmailConfirmation,
    UserResponse,
)

auth = APIRouter(prefix='/auth', tags=['auth'])


@auth.post('/registry')
async def registry(
    account: AccountRegisterSchema,
    auth: AuthUseCases = Depends(get_auth_use_cases),
) -> bool:
    try:
        return auth.register(
            email=account.email,
            username=account.username,
            password=account.password,
        )
    except AccountAlreadyExist as err:
        raise HTTPException(status_code=409, detail=str(err)) from err
    except UsernameAlreadyExist as err:
        raise HTTPException(status_code=409, detail=str(err)) from err


@auth.post('/confirm_email')
async def confirm_email(
    attempt: EmailConfirmation,
    auth: AuthUseCases = Depends(get_auth_use_cases),
) -> bool:
    try:
        res = auth.mail_confirmation(attempt.email, attempt.code)
        if not res:
            raise HTTPException(
                status_code=400, detail='Неверный код подтверждения'
            )
        return res
    except AccountAlreadyExist as err:
        raise HTTPException(status_code=409, detail=str(err)) from err


@auth.post('/login')
async def login(
    account: AccountLoginSchema,
    auth: AuthUseCases = Depends(get_auth_use_cases),
) -> dict:
    try:
        return auth.login(account.email, account.password)
    except AccountNotFound as err:
        raise HTTPException(status_code=400, detail=str(err)) from err
    except InvalidPassword as err:
        raise HTTPException(status_code=400, detail=str(err)) from err
    except AccountIsDeactivate as err:
        raise HTTPException(status_code=403, detail=str(err)) from err


@auth.get('/me', response_model=UserResponse)
async def me(
    token: str = Depends(get_bearer_token),
    auth: AuthUseCases = Depends(get_auth_use_cases),
) -> UserResponse:
    try:
        user = auth.get_current_user(token)
        return UserResponse(
            id=user.id,
            email=user.email,
            username=user.username,
        )
    except (AccountNotFound, ValueError) as err:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Токен отсутствует или недействителен',
        ) from err


@auth.post('/logout', status_code=status.HTTP_204_NO_CONTENT)
async def logout(
    token: str = Depends(get_bearer_token),
    auth: AuthUseCases = Depends(get_auth_use_cases),
) -> Response:
    try:
        auth.logout(token)
    except ValueError as err:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Токен отсутствует или недействителен',
        ) from err
    return Response(status_code=status.HTTP_204_NO_CONTENT)
