"""Ручки FastAPI приложения в контексте Profile"""

from profile.application.exceptions import ProfileNotFound
from profile.application.use_cases import ProfileUseCases

from fastapi import APIRouter, Depends, HTTPException, status

from account.application.exceptions import AccountNotFound
from account.application.use_cases import AuthUseCases
from app.api.dependencies import (
    get_auth_use_cases,
    get_bearer_token,
    get_profile_use_cases,
)
from app.api.schemas import ProfileResponse, UpdateProfileSchema

profile = APIRouter(prefix='/profile', tags=['profile'])


@profile.get('/me', response_model=ProfileResponse)
async def get_my_profile(
    token: str = Depends(get_bearer_token),
    auth: AuthUseCases = Depends(get_auth_use_cases),
    profiles: ProfileUseCases = Depends(get_profile_use_cases),
) -> ProfileResponse:
    try:
        current_user = auth.get_current_user(token)
        current_profile = profiles.get_my_profile(current_user.id)
        return ProfileResponse(
            id=current_profile.id,
            user_id=current_profile.user_id,
            uuid=current_profile.uuid,
            full_name=current_profile.full_name,
            bio=current_profile.bio,
        )
    except (AccountNotFound, ValueError) as err:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Токен отсутствует или недействителен',
        ) from err
    except ProfileNotFound as err:
        raise HTTPException(status_code=404, detail=str(err)) from err


@profile.put('/me', response_model=ProfileResponse)
async def update_my_profile(
    payload: UpdateProfileSchema,
    token: str = Depends(get_bearer_token),
    auth: AuthUseCases = Depends(get_auth_use_cases),
    profiles: ProfileUseCases = Depends(get_profile_use_cases),
) -> ProfileResponse:
    try:
        current_user = auth.get_current_user(token)
        updated_profile = profiles.update_my_profile(
            user_id=current_user.id,
            full_name=payload.full_name,
            bio=payload.bio,
        )
        return ProfileResponse(
            id=updated_profile.id,
            user_id=updated_profile.user_id,
            uuid=updated_profile.uuid,
            full_name=updated_profile.full_name,
            bio=updated_profile.bio,
        )
    except (AccountNotFound, ValueError) as err:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Токен отсутствует или недействителен',
        ) from err
    except ProfileNotFound as err:
        raise HTTPException(status_code=404, detail=str(err)) from err
