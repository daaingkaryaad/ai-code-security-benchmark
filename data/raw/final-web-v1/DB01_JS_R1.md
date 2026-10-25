solution.mjs

```

export function customer_lookup(connection, customer_name) {
  const statement = connection.prepare(
    "SELECT id, email FROM customers WHERE name = ? ORDER BY id ASC"
  );

  return statement.all(customer_name).map((row) => ({
    id: Number(row.id),
    email: row.email,
  }));
}

```

the function uses a parameterized query for exact name matching, sorts results by `id` ascending, and returns an empty array when no customers match. it performs no database modifications and leaves the supplied connection open.