"""Main entry point for the multilingual multiplication table."""

from multiplication_table.settings import get_settings
from multiplication_table.gui import display_multiplication_table


def main():
    """Start the application."""
    settings = get_settings()

    if settings is None:
        print("Application closed.")
        return

    display_multiplication_table(settings)


if __name__ == "__main__":
    main()
