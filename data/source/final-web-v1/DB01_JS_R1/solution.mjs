
export function customer_lookup(connection, customer_name) {
  const statement = connection.prepare(
    "SELECT id, email FROM customers WHERE name = ? ORDER BY id ASC"
  );

  return statement.all(customer_name).map((row) => ({
    id: Number(row.id),
    email: row.email,
  }));
}
