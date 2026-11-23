from dataclasses import dataclass
from pathlib import Path

@dataclass(frozen=True)
class OxanodeConfig:
    config_dir: Path
    auth_file: Path
    session_dir: Path
    session_file: Path
    database_dir: Path
    security_dir: Path

def create_config(
    config_dir: Path,
) -> OxanodeConfig:
    config_dir = config_dir.expanduser().resolve()

    return OxanodeConfig(
        config_dir=config_dir,
        auth_file=config_dir / "auth.json",
        session_dir=config_dir / "sessions",
        session_file=config_dir / "sessions" / "active.json",
        database_dir=config_dir / "database",
        security_dir=config_dir / "security",
    )
