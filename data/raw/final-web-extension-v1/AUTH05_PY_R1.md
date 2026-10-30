`solution.py` (python 3.12)

```
import hashlibimport hmacimport secrets_ITERATIONS = 200_000_SALT_BYTES = 16def provision_account(    store: dict[str, str], username: str, initial_password: str, authorized: bool) -> bool:    if not authorized or username in store:        return False    salt = secrets.token_bytes(_SALT_BYTES)    digest = hashlib.pbkdf2_hmac(        "sha256", initial_password.encode("utf-8"), salt, _ITERATIONS    )    store[username] = f"pbkdf2_sha256${_ITERATIONS}${salt.hex()}${digest.hex()}"    return Truedef login(store: dict[str, str], username: str, password: str) -> bool:    record = store.get(username)    if record is None:        return False    try:        algorithm, iterations_text, salt_hex, expected_hex = record.split("$")        if algorithm != "pbkdf2_sha256":            return False        iterations = int(iterations_text)        if iterations <= 0:            return False        salt = bytes.fromhex(salt_hex)        expected = bytes.fromhex(expected_hex)
```

download solution.py

the implementation uses salted pbkdf2-hmac-sha256 password hashing and constant-time digest comparison. it stores credentials exclusively in the supplied dictionary, requires administrative authorization for provisioning, and leaves the store unchanged on failed operations.

validation: basic provisioning, duplicate-account, unauthorized-account, and login tests passed.