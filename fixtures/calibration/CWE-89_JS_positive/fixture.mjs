export function lookup(connection, name) {
  const sql = "SELECT id FROM customers WHERE name = '" + name + "'";
  return connection.prepare(sql).all();
}
