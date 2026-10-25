download solution.mjs

the implementation uses node.js built-in `crypto` functions and provides all three synchronous named exports:

- `create_account(store, username, password)`
- `rename_account(store, username, password, new_username)`
- `login(store, username, password)`

passwords are stored using `scrypt` with random salts, and verification uses constant-time hash comparison.

successful renames preserve the existing credential record. failed operations leave the store unchanged.

validation: all local tests passed, including account creation, duplicate rejection, password verification, failed renames, and successful renames.