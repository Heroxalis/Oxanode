
import getpass
import json
import os
from pathlib import Path

from app.core.config import OxanodeConfig, create_config
from app.core.installation import get_bootstrap_file, save_installation
from app.core.security import hash_password


def select_storage_location() -> Path:
    print("\nOxanode Initial Setup")
    print("=" * 32)
    print("Choose where Oxanode will store its data:\n")
    print("[1] Default location")
    print("[2] Custom location")

    while True:
        choice = input("\nSelect an option: ").strip()

        if choice == "1":
            return Path.home() / ".local" / "share" / "oxanode"

        if choice == "2":
            location = input("Enter storage directory: ").strip()

            if location:
                return Path(location).expanduser()

        print("Invalid selection. Try again.")


def create_storage(config: OxanodeConfig) -> None:
    directories = [
        config.config_dir,
        config.session_dir,
        config.database_dir,
        config.security_dir,
    ]

    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True, mode=0o700)
        directory.chmod(0o700)


def create_admin_credentials(config: OxanodeConfig) -> None:
    if config.auth_file.exists():
        raise FileExistsError("Administrator credentials already exist.")

    print("\nAdministrator Account")
    print("=" * 32)

    while True:
        username = input("Administrator username: ").strip()

        if 3 <= len(username) <= 64:
            break

        print("Username must be between 3 and 64 characters.")

    while True:
        password = getpass.getpass("Administrator password: ")

        if len(password) < 12:
            print("Password must contain at least 12 characters.")
            continue

        confirmation = getpass.getpass("Confirm password: ")

        if password == confirmation:
            break

        print("Passwords do not match.")

    credentials = {
        "username": username,
        "password_hash": hash_password(password),
    }

    temporary_file = config.auth_file.with_suffix(".tmp")

    file_descriptor = os.open(
        temporary_file,
        os.O_WRONLY | os.O_CREAT | os.O_EXCL,
        0o600,
    )

    try:
        with os.fdopen(file_descriptor, "w", encoding="utf-8") as file:
            json.dump(credentials, file, indent=4)
            file.write("\n")
            file.flush()
            os.fsync(file.fileno())

        os.link(temporary_file, config.auth_file)

    finally:
        temporary_file.unlink(missing_ok=True)

    config.auth_file.chmod(0o600)


def run_initial_setup() -> OxanodeConfig:
    bootstrap_file = get_bootstrap_file()

    if bootstrap_file.exists():
        raise FileExistsError(
            "An Oxanode installation record already exists."
        )

    storage_location = select_storage_location()
    config = create_config(storage_location)

    if config.auth_file.exists():
        raise FileExistsError(
            "An administrator account already exists at this location."
        )

    create_storage(config)
    create_admin_credentials(config)

    try:
        save_installation(config)
    except Exception:
        config.auth_file.unlink(missing_ok=True)
        raise

    print("\nOxanode initial setup completed.")
    print("Administrator account created successfully.")

    return config