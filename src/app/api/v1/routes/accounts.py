from fastapi import APIRouter, Depends, HTTPException, status

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


@router.get("/{user_id}", response_model=UserRead)
async def get_user(
    user_id: int, service: AccountsService = Depends(get_accounts_service)
) -> UserRead:
    user = await service.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user
