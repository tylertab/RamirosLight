from collections.abc import Callable

from fastapi import Depends, HTTPException, status

from app.schemas.user import UserRead
from app.services.accounts import AccountsService, get_accounts_service

from .security import get_current_user


def require_roles(*roles: str) -> Callable[[UserRead], UserRead]:
    normalized = {role.lower() for role in roles}

    async def _checker(user: UserRead = Depends(get_current_user)) -> UserRead:
        if user.role.lower() not in normalized:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient role")
        return user

    return _checker


async def get_current_user_with_model(
    current_user: UserRead = Depends(get_current_user),
    accounts: AccountsService = Depends(get_accounts_service),
) -> UserRead:
    refreshed = await accounts.get_user_by_id(current_user.id)
    if refreshed is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User no longer exists")
    return refreshed
