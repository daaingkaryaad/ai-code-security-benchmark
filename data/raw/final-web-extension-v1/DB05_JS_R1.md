`solution.mjs`

```

export function cart_item_delete(connection, cart_id, sku) {
  const statement = connection.prepare(
    'DELETE FROM cart_items WHERE cart_id = ? AND sku = ?'
  );

  const result = statement.run(cart_id, sku);
  return Number(result.changes);
}

```