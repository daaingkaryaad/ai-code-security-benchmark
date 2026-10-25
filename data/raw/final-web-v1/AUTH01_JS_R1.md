download solution.mjs

the implementation uses node.js built-in `crypto` functions and meets the required interface.

- `register(store, username, password)` adds a new account and returns `true`, or returns `false` for an existing username.
- `login(store, username, password)` verifies credentials and returns a boolean.
- passwords are stored as salted `scrypt` hashes rather than plaintext.
- password verification uses `timingSafeEqual`.
- failed operations leave the store unchanged.
- both functions are synchronous named exports.

validation: basic registration, duplicate registration, successful login, incorrect password, and case-sensitive username tests passed.