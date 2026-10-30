import sqlite3


def profile_update(connection: sqlite3.Connection, username: str, new_email: str) -> int:
    """update the email for an exactly matching username without committing."""
    cursor = connection.execute(
        "UPDATE profiles SET email = ? WHERE username = ?",
        (new_email, username),
    )
    return cursor.rowcount