export function lookup(connection, name) {
  return connection.prepare("SELECT id FROM customers WHERE name = ?").all(name);
}
