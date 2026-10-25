download solution.mjs

```
export function ticket_count(connection, owner, status) {
  const statement = connection.prepare(
    'SELECT COUNT(*) AS count FROM tickets WHERE owner = ? COLLATE BINARY AND status = ? COLLATE BINARY'
  );
  return statement.get(owner, status).count;
}
```

the implementation uses parameterized sql to prevent injection, performs exact case-sensitive comparisons, returns `0` when no tickets match, and leaves the database unchanged.

it uses only the supplied sqlite connection, runs synchronously, and is compatible with node.js 22.13+.

syntax validation passed.