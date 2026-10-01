from datetime import datetime, timedelta, timezone
from typing import Optional, Set
import jwt
from pydantic import BaseModel
from starlette.authentication import (
    AuthCredentials,
    AuthenticationBackend,
    AuthenticationError,
    BaseUser,
)
from starlette.middleware.authentication import AuthenticationMiddleware
from starlette.requests import HTTPConnection
from starlette.responses import JSONResponse, Response
from fastapi import Depends, FastAPI, HTTPException, Request, status
from fastapi.security import OAuth2PasswordRequestForm

SECRET_KEY = "system-dev-secret-key-change-in-production"
ALGORITHM = "HS256"
TOKEN_EXPIRY_MINUTES = 60

class AuthenticatedPrincipal(BaseUser):
    def __init__(self, username: str, scopes: Set[str]) -> None:
        self._username = username
        self._scopes = scopes

    @property
    def is_authenticated(self) -> bool:
        return True

    @property
    def identity(self) -> str:
        return self._username

    @property
    def scopes(self) -> Set[str]:
        return self._scopes

class JWTAuthenticationBackend(AuthenticationBackend):
    async def authenticate(
        self, conn: HTTPConnection
    ) -> Optional[tuple[AuthCredentials, BaseUser]]:
        if "authorization" not in conn.headers:
            return None

        auth_header = conn.headers["authorization"]
        scheme, _, token = auth_header.partition(" ")

        if scheme.lower() != "bearer" or not token:
            raise AuthenticationError("Invalid authorization scheme. Bearer required.")

        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username: str = payload.get("sub")
            scopes: list[str] = payload.get("scopes", [])

            if not username:
                raise AuthenticationError("Token payload missing 'sub' claim.")

            return AuthCredentials(scopes), AuthenticatedPrincipal(
                username=username, scopes=set(scopes)
            )
        except jwt.ExpiredSignatureError:
            raise AuthenticationError("Token signature has expired.")
        except jwt.PyJWTError:
            raise AuthenticationError("Invalid token cryptographic signature.")

def on_auth_error(conn: HTTPConnection, exc: AuthenticationError) -> Response:
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={"error": "authentication_failed", "detail": str(exc)},
        headers={"WWW-Authenticate": "Bearer"},
    )

class ScopeChecker:
    def __init__(self, required_scopes: list[str]) -> None:
        self.required_scopes = set(required_scopes)

    def __call__(self, request: Request) -> None:
        if not request.user.is_authenticated:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Authentication required.",
                headers={"WWW-Authenticate": "Bearer"},
            )

        principal_scopes = set(request.auth.scopes)
        missing_scopes = self.required_scopes - principal_scopes

        if missing_scopes:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Forbidden. Missing required scopes: {sorted(list(missing_scopes))}",
            )

app = FastAPI(title="Authenticated ASGI Service", version="1.0.0")

app.add_middleware(
    AuthenticationMiddleware,
    backend=JWTAuthenticationBackend(),
    on_error=on_auth_error,
)

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in_seconds: int

USER_DATABASE = {
    "admin_user": {
        "password": "admin_password",
        "scopes": ["system:read", "system:write", "admin:access"],
    },
    "operator_user": {
        "password": "operator_password",
        "scopes": ["system:read"],
    },
}

@app.post("/auth/token", response_model=TokenResponse)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user_record = USER_DATABASE.get(form_data.username)
    if not user_record or user_record["password"] != form_data.password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect username or password.",
        )

    now = datetime.now(timezone.utc)
    expiration = now + timedelta(minutes=TOKEN_EXPIRY_MINUTES)

    claims = {
        "sub": form_data.username,
        "scopes": user_record["scopes"],
        "iat": now,
        "exp": expiration,
    }
    encoded_token = jwt.encode(claims, SECRET_KEY, algorithm=ALGORITHM)

    return TokenResponse(
        access_token=encoded_token,
        expires_in_seconds=TOKEN_EXPIRY_MINUTES * 60,
    )

@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.now(timezone.utc).isoformat()}

@app.get("/profile/me")
async def get_current_profile(request: Request):
    if not request.user.is_authenticated:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required.",
        )
    return {
        "username": request.user.identity,
        "granted_scopes": list(request.auth.scopes),
    }

@app.get(
    "/admin/metrics",
    dependencies=[Depends(ScopeChecker(["admin:access"]))],
)
async def get_admin_metrics(request: Request):
    return {
        "status": "operational",
        "authenticated_admin": request.user.identity,
        "active_tenants": 1,
    }
