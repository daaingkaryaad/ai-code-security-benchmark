download solution.py

```
import sqlite3def cart_item_delete(connection: sqlite3.Connection, cart_id: str, sku: str) -> int:    cursor = connection.execute(        "DELETE FROM cart_items WHERE cart_id = ? AND sku = ?",        (cart_id, sku),    )    return cursor.rowcount
```

the function uses a parameterized query to delete the exact matching cart item and returns `1` if deleted or `0` if no matching row exists.

it does not commit, roll back, modify connection settings, or close the supplied connection.