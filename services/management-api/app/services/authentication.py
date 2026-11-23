
import hashlib
import json
import secrets
from datetime import datetime, timedelta, timezone

from app.core.config import OxanodeConfig
from app.core.security import verify_password


SESSION_DURATION = timedelta(hours=12)


class AuthenticationService:
    def __init__(self, config: OxanodeConfig):
        self.config = config

    def load_admin_credentials(self) -> dict | None:
        auth_file = self.config.auth_file

        if not auth_file.is_file():
            return None

        try:
            with auth_file.open("r", encoding="utf-8") as file:
                credentials = json.load(file)

            if not isinstance(credentials, dict):
                return None

            username = credentials.get("username")
            password_hash = credentials.get("password_hash")

            if not isinstance(username, str):
                return None

            if not isinstance(password_hash, str):
                return None

            return credentials

        except (OSError, json.JSONDecodeError):
            return None

    @staticmethod
    def _hash_token(token: str) -> str:
        return hashlib.sha256(token.encode("utf-8")).hexdigest()

    def create_session(self) -> str:
        session_dir = self.config.session_dir
        session_dir.mkdir(parents=True, exist_ok=True, mode=0o700)
        session_dir.chmod(0o700)

        token = secrets.token_urlsafe(32)
        now = datetime.now(timezone.utc)

        session = {
            "token_hash": self._hash_token(token),
            "created_at": now.isoformat(),
            "expires_at": (now + SESSION_DURATION).isoformat()
        }

        temporary_file = self.config.session_file.with_suffix(".tmp")

        with temporary_file.open("w", encoding="utf-8") as file:
            json.dump(session, file)

        temporary_file.chmod(0o600)
        temporary_file.replace(self.config.session_file)

        return token

    def verify_session(self, token: str) -> bool:
        session_file = self.config.session_file

        if not session_file.is_file():
            return False

        try:
            with session_file.open("r", encoding="utf-8") as file:
                session = json.load(file)

            stored_hash = session.get("token_hash")
            expires_at = datetime.fromisoformat(session["expires_at"])

            if not isinstance(stored_hash, str):
                return False

            if not secrets.compare_digest(
                stored_hash,
                self._hash_token(token)
            ):
                return False

            if datetime.now(timezone.utc) >= expires_at:
                self.invalidate_session()
                return False

            return True

        except (OSError, ValueError, KeyError, TypeError, json.JSONDecodeError):
            return False

    def invalidate_session(self) -> None:
        try:
            self.config.session_file.unlink(missing_ok=True)
        except OSError:
            pass

    def authenticate_admin(self, username: str, password: str) -> bool:
        credentials = self.load_admin_credentials()

        if credentials is None:
            return False

        if not secrets.compare_digest(
            username,
            credentials["username"]
        ):
            return False

        return verify_password(
            password,
            credentials["password_hash"]
        )
