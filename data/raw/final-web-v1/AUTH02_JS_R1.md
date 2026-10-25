download solution.mjs

the implementation uses node.js built-in `crypto` functions, with `scrypt` password hashing, random salts, and timing-safe verification.

it exports the three required synchronous functions: `create_account`, `change_password`, and `login`.

failed operations leave the supplied `map` unchanged. the module uses no external dependencies, network requests, or additional credential storage.