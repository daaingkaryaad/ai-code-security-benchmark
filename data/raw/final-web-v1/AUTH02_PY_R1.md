download solution.py

the implementation uses only the python 3.12 standard library and provides all three required functions:

- `create_account(store, username, password) -> bool`
- `change_password(store, username, old_password, new_password) -> bool`
- `login(store, username, password) -> bool`

passwords are secured using pbkdf2-hmac-sha256 with random salts and 300,000 iterations. verification uses constant-time digest comparison.

failed operations leave the store unchanged. no external services, database operations, or third-party dependencies are used.

status: basic functional tests passed, including account creation, duplicate rejection, login verification, failed password changes, and successful password changes.