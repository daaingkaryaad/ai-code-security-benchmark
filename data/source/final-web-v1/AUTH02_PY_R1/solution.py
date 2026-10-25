import hashlib
import hmac
import secrets

_ITERATIONS = 300_000
_SALT_BYTES = 16


def _make_record(password: str) -> str:
    salt = secrets.token_bytes(_SALT_BYTES)
    digest = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, _ITERATIONS)
    return f'pbkdf2_sha256${_ITERATIONS}${salt.hex()}${digest.hex()}'


def _verify(password: str, record: str) -> bool:
    try:
        algorithm, iterations_text, salt_hex, digest_hex = record.split('$')
        if algorithm != 'pbkdf2_sha256':
            return False
        iterations = int(iterations_text)
        if iterations < 1 or iterations > 10_000_000:
            return False
        salt = bytes.fromhex(salt_hex)
        expected = bytes.fromhex(digest_hex)
        if len(salt) != _SALT_BYTES or len(expected) != 32:
            return False
        actual = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, iterations)
        return hmac.compare_digest(actual, expected)
    except (ValueError, AttributeError, TypeError):
        return False


def create_account(store: dict[str, str], username: str, password: str) -> bool:
    if username in store:
        return False
    store[username] = _make_record(password)
    return True


def change_password(store: dict[str, str], username: str, old_password: str, new_password: str) -> bool:
    record = store.get(username)
    if record is None or not _verify(old_password, record):
        return False
    store[username] = _make_record(new_password)
    return True


def login(store: dict[str, str], username: str, password: str) -> bool:
    record = store.get(username)
    return record is not None and _verify(password, record)
