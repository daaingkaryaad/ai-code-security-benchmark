here's the implementation for `solution.mjs`, compatible with node.js 22.13+ and the built-in `node:sqlite` module.

```

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

```

this uses `instr()` for case-sensitive literal substring matching, so `%` and `_` are treated as ordinary characters. the query is parameterized, synchronous, read-only, and returns an empty array when no products match.

download solution.mjs

the downloadable version also converts sqlite result rows into ordinary javascript objects containing exactly `id`, `name`, and `price`. it passed local tests for literal matching, case sensitivity, price filtering, and empty results.