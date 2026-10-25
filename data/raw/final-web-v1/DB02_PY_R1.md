here's the complete python 3.12 implementation for `solution.py`.

```
import sqlite3def product_search(    connection: sqlite3.Connection,    term: str,    max_price: float) -> list[dict[str, object]]:    cursor = connection.execute(        """        SELECT id, name, price        FROM products        WHERE instr(name COLLATE BINARY, ?) > 0          AND price <= ?        ORDER BY id ASC        """,        (term, max_price)    )    return [        {            "id": row[0],            "name": row[1],            "price": row[2]        }        for row in cursor    ]
```

download solution.py

the implementation uses `instr()` for case-sensitive literal substring matching, including `%` and `_`. it uses parameterized sql, sorts by ascending `id`, and leaves the database unchanged.

tested successfully with sqlite.