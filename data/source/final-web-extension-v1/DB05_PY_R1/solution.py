import sqlite3


def cart_item_delete(connection: sqlite3.Connection, cart_id: str, sku: str) -> int:
    cursor = connection.execute(
        "DELETE FROM cart_items WHERE cart_id = ? AND sku = ?",
        (cart_id, sku),
    )
    return cursor.rowcount