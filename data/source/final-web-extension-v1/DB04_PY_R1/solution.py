import sqlite3


def order_filter(
    connection: sqlite3.Connection, status: str, min_total: float
) -> list[dict[str, object]]:
    cursor = connection.execute(
        """
        SELECT id, total
        FROM orders
        WHERE status = ? COLLATE BINARY AND total >= ?
        ORDER BY id ASC
        """,
        (status, min_total),
    )
    return [{"id": row[0], "total": row[1]} for row in cursor]