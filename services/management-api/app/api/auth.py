
import os

from fastapi import APIRouter, HTTPException, Request, Response, status

from app.schemas.auth import LoginRequest, LoginResponse, AdminResponse

router = APIRouter(prefix="/api/auth", tags=["Authentication"])

SESSION_COOKIE = "oxanode_session"
SESSION_MAX_AGE = 12 * 60 * 60

COOKIE_SECURE = os.getenv("OXANODE_COOKIE_SECURE", "false").lower() == "true"

def get_auth_service(request: Request):
    auth_service = getattr(request.app.state, "auth_service", None)

    if auth_service is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Authentication service is unavailable.",
        )

    return auth_service

def get_rate_limiter(request: Request):
    rate_limiter = getattr(request.app.state, "rate_limiter", None)

    if rate_limiter is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Rate limiting service is unavailable.",
        )

    return rate_limiter

@router.post("/login", response_model=LoginResponse)
async def login(
    credentials: LoginRequest,
    request: Request,
    response: Response,
):
    auth_service = get_auth_service(request)
    rate_limiter = get_rate_limiter(request)

    client_ip = request.client.host if request.client else "unknown"

    retry_after = rate_limiter.consume_attempt(
        client_ip,
        credentials.username,
    )

    if retry_after is not None:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Too many login attempts. Please try again later.",
            headers={"Retry-After": str(retry_after)},
        )

    if not auth_service.authenticate_admin(
        credentials.username,
        credentials.password,
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password.",
        )

    rate_limiter.clear_attempts(
        client_ip,
        credentials.username,
    )

    token = auth_service.create_session()

    response.set_cookie(
        key=SESSION_COOKIE,
        value=token,
        max_age=SESSION_MAX_AGE,
        httponly=True,
        secure=COOKIE_SECURE,
        samesite="strict",
        path="/",
    )

    return LoginResponse(
        authenticated=True,
        message="Authentication successful.",
    )

@router.post("/logout", response_model=LoginResponse)
async def logout(request: Request, response: Response):
    auth_service = get_auth_service(request)
    token = request.cookies.get(SESSION_COOKIE)

    if token and auth_service.verify_session(token):
        auth_service.invalidate_session()

    response.delete_cookie(
        key=SESSION_COOKIE,
        path="/",
        httponly=True,
        secure=COOKIE_SECURE,
        samesite="strict",
    )

    return LoginResponse(
        authenticated=False,
        message="Session terminated.",
    )

@router.get("/me", response_model=AdminResponse)
async def get_current_admin(request: Request):
    auth_service = get_auth_service(request)
    token = request.cookies.get(SESSION_COOKIE)

    if not token or not auth_service.verify_session(token):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required.",
        )

    credentials = auth_service.load_admin_credentials()

    if credentials is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Administrator credentials are unavailable.",
        )

    return AdminResponse(
        username=credentials["username"],
        authenticated=True,
    )
