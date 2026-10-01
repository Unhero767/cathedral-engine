# cathedral_engine/app/routes/auth.py

from fastapi import APIRouter, HTTPException, Request, status
from pydantic import BaseModel

from cathedral_engine.app.logging.ash_archive import log_auth_event, log_iam_event
from cathedral_engine.app.logging.constants import EventType

router = APIRouter()


class LoginRequest(BaseModel):
    username: str
    password: str


class RoleChangeRequest(BaseModel):
    new_role: str


@router.post("/auth/login")
async def login(request: Request, payload: LoginRequest):
    is_valid = payload.username == "admin" and payload.password == "super-secret"

    if not is_valid:
        await log_auth_event(
            request,
            status_code=status.HTTP_401_UNAUTHORIZED,
            event_type=EventType.AUTH_LOGIN_FAILED,
            error_code="invalid_credentials",
            actor_user_id=None,
        )
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )

    user_id = "user_12345"

    await log_auth_event(
        request,
        status_code=status.HTTP_200_OK,
        event_type=EventType.AUTH_LOGIN_SUCCEEDED,
        error_code=None,
        actor_user_id=user_id,
    )

    return {"access_token": "fake-token", "token_type": "bearer"}


@router.patch("/users/{user_id}/role")
async def change_user_role(
    user_id: str,
    payload: RoleChangeRequest,
    request: Request,
):
    actor_user_id = "admin_99"
    previous_role = "standard_user"
    new_role = payload.new_role

    await log_iam_event(
        request,
        status_code=200,
        event_type=EventType.IAM_ROLE_UPDATED,
        actor_user_id=actor_user_id,
        target_user_id=user_id,
        previous_role=previous_role,
        new_role=new_role,
    )

    return {"user_id": user_id, "previous_role": previous_role, "new_role": new_role}
