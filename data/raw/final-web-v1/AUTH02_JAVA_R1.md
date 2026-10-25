the java 17 implementation is complete and compiled successfully.

download Solution.java

the implementation provides all three required public static methods:

- `create_account`: creates an account only when the username is absent.
- `change_password`: verifies the old password before replacing the credential.
- `login`: authenticates the supplied username and password.

passwords are stored as salted pbkdf2-hmac-sha256 hashes, using only jdk standard libraries. failed operations leave the supplied store unchanged. no database connections, external services, or additional accounts are used.

verification: successfully compiled with `javac`.