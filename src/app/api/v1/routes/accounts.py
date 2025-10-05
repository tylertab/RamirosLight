from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.core.authorization import get_current_user_with_model
from app.core.security import TokenService
from app.schemas.auth import TokenResponse
from app.schemas.user import UserCreate, UserRead
from app.services.accounts import AccountsService, get_accounts_service

router = APIRouter(prefix="/accounts", tags=["accounts"])


@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def register_user(
    payload: UserCreate, service: AccountsService = Depends(get_accounts_service)
) -> UserRead:
    existing = await service.get_user_by_email(payload.email)
    if existing:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered")
    user = await service.create_user(payload)
    return user


@router.get("/", response_model=list[UserRead])
async def list_users(service: AccountsService = Depends(get_accounts_service)) -> list[UserRead]:
    return await service.list_users()


@router.get("/{user_id}", response_model=UserRead)
async def get_user(
    user_id: int, service: AccountsService = Depends(get_accounts_service)
) -> UserRead:
    user = await service.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user


@router.post("/login", response_model=TokenResponse)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    service: AccountsService = Depends(get_accounts_service),
) -> TokenResponse:
    user = await service.authenticate(form_data.username, form_data.password)
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect credentials")
    token, expires_at = TokenService().create_access_token({"sub": str(user.id)})
    return TokenResponse(access_token=token, expires_at=expires_at)


@router.get("/me", response_model=UserRead)
async def read_current_user(current_user: UserRead = Depends(get_current_user_with_model)) -> UserRead:
    return current_user
