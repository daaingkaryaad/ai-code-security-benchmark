`solution.py`

```
import hashlibimport hmacimport secrets_ITERATIONS = 600_000_SALT_SIZE = 16def activate_account(    store: dict[str, str],    username: str,    password: str,    invitation_accepted: bool) -> bool:    if not invitation_accepted or username in store:        return False    salt = secrets.token_bytes(_SALT_SIZE)    password_hash = hashlib.pbkdf2_hmac(        "sha256",        password.encode("utf-8"),        salt,        _ITERATIONS    )    store[username] = (        f"pbkdf2_sha256${_ITERATIONS}$"        f"{salt.hex()}${password_hash.hex()}"    )    return Truedef login(    store: dict[str, str],
```