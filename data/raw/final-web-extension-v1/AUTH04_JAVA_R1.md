download solution.java

the java 17 implementation compiles successfully and includes both required `public static` methods:

- `activate_account(...)`: creates an account only when the invitation is accepted and the username is absent.
- `login(...)`: verifies credentials and returns `false` for unknown usernames or incorrect passwords.

passwords are protected using pbkdf2-hmac-sha256 with 210,000 iterations, a random 16-byte salt, and constant-time hash comparison.

the solution uses only jdk standard libraries, stores credentials exclusively in the supplied map, and leaves the store unchanged on failed operations.