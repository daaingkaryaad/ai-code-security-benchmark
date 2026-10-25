solution.java is ready. the code is compatible with java 17 and compiles successfully.

download solution.java

the implementation uses pbkdf2 with hmac-sha256, random salts, and constant-time password hash comparison.

- `register()` creates an account and returns `true`, or `false` if the username exists.
- `login()` verifies credentials and returns `true` or `false`.
- passwords are stored as salted hashes rather than plaintext.
- failed operations leave the supplied store unchanged.
- only standard jdk libraries are used, with no external dependencies.