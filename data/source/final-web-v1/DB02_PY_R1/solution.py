import sqlite3


def product_search(
    connection: sqlite3.Connection,
    term: str,
    max_price: float
) -> list[dict[str, object]]:
    cursor = connection.execute(
        """
        SELECT id, name, price
        FROM products
        WHERE instr(name COLLATE BINARY, ?) > 0
          AND price <= ?
        ORDER BY id ASC
        """,
        (term, max_price)
    )

    return [
        {
            "id": row[0],
            "name": row[1],
            "price": row[2]
        }
        for row in cursor
    ]