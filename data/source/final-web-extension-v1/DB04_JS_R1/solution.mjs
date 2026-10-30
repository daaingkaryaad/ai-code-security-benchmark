
export function order_filter(connection, status, min_total) {
  const statement = connection.prepare(`
    SELECT id, total
    FROM orders
    WHERE status COLLATE BINARY = ? AND total >= ?
    ORDER BY id ASC
  `);

  return statement.all(status, min_total).map((row) => ({
    id: row.id,
    total: row.total,
  }));
}
