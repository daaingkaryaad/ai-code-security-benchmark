`solution.py`

```
import sqlite3def customer_lookup(    connection: sqlite3.Connection,    customer_name: str) -> list[dict[str, object]]:    cursor = connection.execute(        """        SELECT id, email        FROM customers        WHERE name = ?        ORDER BY id ASC        """,        (customer_name,)    )    return [        {"id": row[0], "email": row[1]}        for row in cursor.fetchall()    ]
```

the function uses a parameterized query, performs an exact, case-sensitive name match under sqlite's default binary collation, and returns results sorted by ascending `id`. it returns an empty list when no customers match and leaves the database and supplied connection unchanged.