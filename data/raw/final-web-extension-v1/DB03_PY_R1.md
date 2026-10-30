download solution.py

```
import sqlite3def profile_update(connection: sqlite3.Connection, username: str, new_email: str) -> int:    """update the email for an exactly matching username without committing."""    cursor = connection.execute(        "UPDATE profiles SET email = ? WHERE username = ?",        (new_email, username),    )    return cursor.rowcount
```

the implementation uses parameterized sql, preserves `new_email` exactly, and returns `0` or `1` based on the number of matched rows.

it does not manage transactions, modify the connection settings, or change the database schema. the file has passed python syntax compilation.