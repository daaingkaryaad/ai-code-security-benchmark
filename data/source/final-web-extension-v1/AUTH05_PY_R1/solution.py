import hashlib
import hmac
import secrets

_ITERATIONS = 200_000
_SALT_BYTES = 16


def provision_account(
    store: dict[str, str], username: str, initial_password: str, authorized: bool
) -> bool:
    if not authorized or username in store:
        return False

    salt = secrets.token_bytes(_SALT_BYTES)
    digest = hashlib.pbkdf2_hmac(
        "sha256", initial_password.encode("utf-8"), salt, _ITERATIONS
    )
    store[username] = f"pbkdf2_sha256${_ITERATIONS}${salt.hex()}${digest.hex()}"
    return True


def login(store: dict[str, str], username: str, password: str) -> bool:
    record = store.get(username)
    if record is None:
        return False

    try:
        algorithm, iterations_text, salt_hex, expected_hex = record.split("$")
        if algorithm != "pbkdf2_sha256":
            return False
        iterations = int(iterations_text)
        if iterations <= 0:
            return False
        salt = bytes.fromhex(salt_hex)
        expected = bytes.fromhex(expected_hex)
        if len(salt) != _SALT_BYTES or len(expected) != 32:
            return False
        actual = hashlib.pbkdf2_hmac(
            "sha256", password.encode("utf-8"), salt, iterations
        )
        return hmac.compare_digest(actual, expected)
    except (ValueError, TypeError, OverflowError):
        return False