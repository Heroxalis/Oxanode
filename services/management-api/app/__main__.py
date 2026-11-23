import sys

from app.core.initial_setup import run_initial_setup
from app.core.installation import is_initialized


def main():
    if is_initialized():
        print("Oxanode is already initialized.")
        print("Use the recovery procedure if you need to reset it.")
        sys.exit(1)

    try:
        run_initial_setup()
    except KeyboardInterrupt:
        print("\nSetup cancelled.")
        sys.exit(1)
    except Exception as error:
        print(f"\nSetup failed: {error}")
        sys.exit(1)


if __name__ == "__main__":
    main()
