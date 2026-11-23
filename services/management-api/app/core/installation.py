
import json
import os
import tempfile
from pathlib import Path

from app.core.config import OxanodeConfig, create_config


def get_bootstrap_file() -> Path:
    config_home = Path(
        os.environ.get("XDG_CONFIG_HOME", Path.home() / ".config")
    ).expanduser()

    return config_home / "oxanode" / "installation.json"


def save_installation(config: OxanodeConfig) -> None:
    bootstrap_file = get_bootstrap_file()
    bootstrap_dir = bootstrap_file.parent

    bootstrap_dir.mkdir(parents=True, exist_ok=True, mode=0o700)
    bootstrap_dir.chmod(0o700)

    if bootstrap_file.exists():
        raise FileExistsError("Oxanode installation already exists.")

    payload = {
        "storage_location": str(config.config_dir.resolve())
    }

    descriptor, temporary_path = tempfile.mkstemp(
        prefix=".installation-",
        suffix=".tmp",
        dir=bootstrap_dir,
    )

    try:
        os.fchmod(descriptor, 0o600)

        with os.fdopen(descriptor, "w", encoding="utf-8") as file:
            json.dump(payload, file, indent=4)
            file.write("\n")
            file.flush()
            os.fsync(file.fileno())

        os.link(temporary_path, bootstrap_file)
        bootstrap_file.chmod(0o600)

    finally:
        Path(temporary_path).unlink(missing_ok=True)


def load_installation() -> OxanodeConfig | None:
    bootstrap_file = get_bootstrap_file()

    try:
        with bootstrap_file.open("r", encoding="utf-8") as file:
            installation = json.load(file)

        if not isinstance(installation, dict):
            return None

        storage_location = installation.get("storage_location")

        if not isinstance(storage_location, str) or not storage_location:
            return None

        config = create_config(Path(storage_location))

        if not config.config_dir.is_dir():
            return None

        return config

    except (OSError, ValueError, TypeError, AttributeError):
        return None


def is_initialized() -> bool:
    config = load_installation()

    if config is None:
        return False

    return config.auth_file.is_file()
