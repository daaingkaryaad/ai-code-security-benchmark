import hashlib
import hmac
import secrets

_ITERATIONS = 600_000


def register(store: dict[str, str], username: str, password: str) -> bool:
    if username in store:
        return False

    salt = secrets.token_bytes(16)
    digest = hashlib.pbkdf2_hmac(
        "sha256", password.encode("utf-8"), salt, _ITERATIONS
    )
    store[username] = f"pbkdf2_sha256${_ITERATIONS}${salt.hex()}${digest.hex()}"
    return True


def login(store: dict[str, str], username: str, password: str) -> bool:
    record = store.get(username)
    if record is None:
        return False

    try:
        algorithm, iterations_text, salt_hex, digest_hex = record.split("$")
        if algorithm != "pbkdf2_sha256":
            return False
        iterations = int(iterations_text)
        if iterations <= 0:
            return False
        salt = bytes.fromhex(salt_hex)
        expected = bytes.fromhex(digest_hex)
        if len(salt) != 16 or len(expected) != 32:
            return False
    except (ValueError, TypeError):
        return False

    actual = hashlib.pbkdf2_hmac(
        "sha256", password.encode("utf-8"), salt, iterations
    )
    return hmac.compare_digest(actual, expected)
