import os


def get_database_url() -> str:
    """Get defined db connection url.

    Returns:
        connection url (aka connection string) from DATABASE_URL env var.
            Default to in-memory sqlite database.

    """
    return os.environ.get("DATABASE_URL", "sqlite:///database.db")
