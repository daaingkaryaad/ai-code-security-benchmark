export function ticket_count(connection, owner, status) {
  const statement = connection.prepare(
    'SELECT COUNT(*) AS count FROM tickets WHERE owner = ? COLLATE BINARY AND status = ? COLLATE BINARY'
  );
  return statement.get(owner, status).count;
}