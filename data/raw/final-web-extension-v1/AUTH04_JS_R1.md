download solution.mjs

the implementation uses node.js 22 built-in modules and provides both required synchronous named exports.

- `activate_account(store, username, password, invitation_accepted)` creates an account only when the invitation is accepted and the username is absent.
- `login(store, username, password)` verifies credentials and returns a boolean.
- passwords are protected using `scrypt` with a random 16-byte salt.
- password hashes are compared using `timingSafeEqual`.
- failed operations leave the store unchanged.
- no external dependencies, persistent storage, or demonstration accounts.

validation: passed basic tests covering activation, duplicate accounts, rejected invitations, successful login, incorrect passwords, and unknown usernames.