download solution.mjs

```

export function profile_update(connection, username, new_email) {
  const statement = connection.prepare(
    'UPDATE profiles SET email = ? WHERE username = ?'
  );
  const result = statement.run(new_email, username);
  return result.changes;
}

```

the implementation uses a parameterized sqlite query, preserves the supplied email exactly, and returns the number of updated rows (`0` or `1`). it does not manage the connection or transaction.