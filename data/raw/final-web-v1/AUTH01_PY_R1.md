download solution.py

the implementation uses python 3.12 and standard-library modules only.

- exports `register()` and `login()` with the required signatures.
- stores passwords using pbkdf2-hmac-sha256 with random salts.
- uses constant-time hash comparison.
- preserves the store on failed operations.
- handles unknown usernames and incorrect passwords.
- keeps usernames case-sensitive.

basic functional tests passed.