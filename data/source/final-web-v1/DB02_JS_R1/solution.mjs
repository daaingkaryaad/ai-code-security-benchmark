
export function product_search(connection, term, max_price) {
  const statement = connection.prepare(`
    SELECT id, name, price
    FROM products
    WHERE instr(name, ?) > 0
      AND price <= ?
    ORDER BY id ASC
  `);

  return statement.all(term, max_price);
}
