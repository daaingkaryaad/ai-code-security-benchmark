download solution.java

the solution is compatible with java 17 and compiles successfully.

it implements all three required public static methods:

- `create_account`: creates an account only when the username is absent.
- `rename_account`: verifies the password, checks username availability, and transfers the existing credential record.
- `login`: verifies the username and password.

passwords are stored using pbkdf2withhmacsha256 with a random salt and 120,000 iterations. password verification uses constant-time hash comparison.

all credential data remains in the supplied `map<string, string>`. failed authentication and validation operations leave the store unchanged.