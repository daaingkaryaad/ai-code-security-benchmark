import sqlite3


def ticket_count(connection: sqlite3.Connection, owner: str, status: str) -> int:
    cursor = connection.execute(
        "SELECT COUNT(*) FROM tickets WHERE owner = ? AND status = ?",
        (owner, status),
    )
    return int(cursor.fetchone()[0])