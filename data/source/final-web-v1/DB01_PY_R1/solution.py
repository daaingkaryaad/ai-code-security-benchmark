
import sqlite3


def customer_lookup(
    connection: sqlite3.Connection,
    customer_name: str
) -> list[dict[str, object]]:
    cursor = connection.execute(
        """
        SELECT id, email
        FROM customers
        WHERE name = ?
        ORDER BY id ASC
        """,
        (customer_name,)
    )

    return [
        {"id": row[0], "email": row[1]}
        for row in cursor.fetchall()
    ]
