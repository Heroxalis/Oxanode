
import hashlib
import math
import sqlite3
import time

from app.core.config import OxanodeConfig


RATE_LIMIT_WINDOW = 15 * 60
BLOCK_DURATION = 15 * 60

IP_LIMIT = 10
ACCOUNT_LIMIT = 5


class LoginRateLimiter:
    def __init__(self, config: OxanodeConfig):
        self.database_path = config.database_dir / "rate_limits.sqlite3"

    def _connect(self) -> sqlite3.Connection:
        self.database_path.parent.mkdir(
            parents=True,
            exist_ok=True,
            mode=0o700,
        )
        self.database_path.parent.chmod(0o700)

        connection = sqlite3.connect(
            self.database_path,
            timeout=5,
            isolation_level=None,
        )

        connection.execute("PRAGMA busy_timeout = 5000")
        self.database_path.chmod(0o600)

        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS login_attempts (
                scope TEXT NOT NULL,
                key_hash TEXT NOT NULL,
                window_started REAL NOT NULL,
                attempts INTEGER NOT NULL DEFAULT 0,
                blocked_until REAL NOT NULL DEFAULT 0,
                PRIMARY KEY (scope, key_hash)
            )
            """
        )

        return connection

    @staticmethod
    def _hash_key(scope: str, value: str) -> str:
        data = f"{scope}:{value}".encode("utf-8")
        return hashlib.sha256(data).hexdigest()

    def consume_attempt(
        self,
        ip_address: str,
        username: str,
    ) -> int | None:
        now = time.time()

        buckets = [
            (
                "ip",
                self._hash_key("ip", ip_address),
                IP_LIMIT,
            ),
            (
                "account",
                self._hash_key(
                    "account",
                    f"{ip_address}\0{username}",
                ),
                ACCOUNT_LIMIT,
            ),
        ]

        connection = self._connect()

        try:
            connection.execute("BEGIN IMMEDIATE")

            states = []

            # Read and prepare both rate-limit buckets.
            for scope, key_hash, limit in buckets:
                row = connection.execute(
                    """
                    SELECT window_started, attempts, blocked_until
                    FROM login_attempts
                    WHERE scope = ? AND key_hash = ?
                    """,
                    (scope, key_hash),
                ).fetchone()

                if row is None:
                    window_started = now
                    attempts = 0
                    blocked_until = 0

                else:
                    window_started, attempts, blocked_until = row

                    if blocked_until > now:
                        connection.commit()
                        return max(1, math.ceil(blocked_until - now))

                    if now - window_started >= RATE_LIMIT_WINDOW:
                        window_started = now
                        attempts = 0
                        blocked_until = 0

                states.append(
                    (
                        scope,
                        key_hash,
                        limit,
                        window_started,
                        attempts,
                    )
                )

            # Check whether either bucket has reached its limit.
            for (
                scope,
                key_hash,
                limit,
                window_started,
                attempts,
            ) in states:
                if attempts >= limit:
                    blocked_until = now + BLOCK_DURATION

                    connection.execute(
                        """
                        UPDATE login_attempts
                        SET blocked_until = ?
                        WHERE scope = ? AND key_hash = ?
                        """,
                        (blocked_until, scope, key_hash),
                    )

                    connection.commit()
                    return BLOCK_DURATION

            # Count this login attempt in both buckets.
            for (
                scope,
                key_hash,
                limit,
                window_started,
                attempts,
            ) in states:
                connection.execute(
                    """
                    INSERT INTO login_attempts (
                        scope,
                        key_hash,
                        window_started,
                        attempts,
                        blocked_until
                    )
                    VALUES (?, ?, ?, ?, 0)
                    ON CONFLICT(scope, key_hash)
                    DO UPDATE SET
                        window_started = excluded.window_started,
                        attempts = excluded.attempts,
                        blocked_until = 0
                    """,
                    (
                        scope,
                        key_hash,
                        window_started,
                        attempts + 1,
                    ),
                )

            connection.commit()
            return None

        except Exception:
            connection.rollback()
            raise

        finally:
            connection.close()

    def clear_attempts(
        self,
        ip_address: str,
        username: str,
    ) -> None:
        buckets = [
            (
                "ip",
                self._hash_key("ip", ip_address),
            ),
            (
                "account",
                self._hash_key(
                    "account",
                    f"{ip_address}\0{username}",
                ),
            ),
        ]

        connection = self._connect()

        try:
            connection.execute("BEGIN IMMEDIATE")

            for scope, key_hash in buckets:
                connection.execute(
                    """
                    DELETE FROM login_attempts
                    WHERE scope = ? AND key_hash = ?
                    """,
                    (scope, key_hash),
                )

            connection.commit()

        except Exception:
            connection.rollback()
            raise

        finally:
            connection.close()
