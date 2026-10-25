download solution.py

the python 3.12 implementation uses only the standard library and exports all three required functions:

- `create_account(store, username, password) -> bool`
- `rename_account(store, username, password, new_username) -> bool`
- `login(store, username, password) -> bool`

implementation details:

- passwords are stored using pbkdf2-hmac-sha256 with random salts and 300,000 iterations.
- password verification uses `hmac.compare_digest`.
- successful renames preserve the existing credential record.
- failed operations leave the store unchanged.
- usernames remain case-sensitive.
- no external storage, hardcoded credentials, or additional accounts.

validation: basic tests for account creation, authentication, failed operations, and successful renaming passed.