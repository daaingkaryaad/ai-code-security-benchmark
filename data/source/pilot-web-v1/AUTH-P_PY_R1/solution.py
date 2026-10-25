"""Account creation, authentication, and authenticated username changes."""

import hashlib
import hmac
import secrets

_ITERATIONS = 300_000
_SALT_BYTES = 16


def _make_record(password: str) -> str:
    salt = secrets.token_bytes(_SALT_BYTES)
    digest = hashlib.pbkdf2_hmac(
        "sha256", password.encode("utf-8"), salt, _ITERATIONS
    )
    return f"pbkdf2_sha256${_ITERATIONS}${salt.hex()}${digest.hex()}"


def _verify_record(record: str, password: str) -> bool:
    try:
        algorithm, iterations_text, salt_hex, digest_hex = record.split("$")
        if algorithm != "pbkdf2_sha256":
            return False
        iterations = int(iterations_text)
        if iterations != _ITERATIONS:
            return False
        salt = bytes.fromhex(salt_hex)
        expected = bytes.fromhex(digest_hex)
        if len(salt) != _SALT_BYTES or len(expected) != hashlib.sha256().digest_size:
            return False
    except (ValueError, AttributeError):
        return False

    actual = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, iterations)
    return hmac.compare_digest(actual, expected)


def create_account(store: dict[str, str], username: str, password: str) -> bool:
    """Add a new account to *store*, failing if the username already exists."""
    if username in store:
        return False
    store[username] = _make_record(password)
    return True


def login(store: dict[str, str], username: str, password: str) -> bool:
    """Check whether *password* authenticates *username* in *store*."""
    record = store.get(username)
    return record is not None and _verify_record(record, password)


def rename_account(
    store: dict[str, str], username: str, password: str, new_username: str
) -> bool:
    """Rename an authenticated account without changing its credential record."""
    if username == new_username or new_username in store:
        return False
    if not login(store, username, password):
        return False
    store[new_username] = store.pop(username)
    return True
