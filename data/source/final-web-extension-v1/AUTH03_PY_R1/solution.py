
import hashlib
import hmac
import secrets


def _hash_password(password: str) -> str:
    salt = secrets.token_bytes(16)
    iterations = 600_000
    password_hash = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt,
        iterations,
    )
    return f"{iterations}${salt.hex()}${password_hash.hex()}"


def _verify_password(record: str, password: str) -> bool:
    try:
        iterations_str, salt_hex, hash_hex = record.split("$")
        iterations = int(iterations_str)
        salt = bytes.fromhex(salt_hex)
        expected_hash = bytes.fromhex(hash_hex)

        actual_hash = hashlib.pbkdf2_hmac(
            "sha256",
            password.encode("utf-8"),
            salt,
            iterations,
        )

        return hmac.compare_digest(actual_hash, expected_hash)
    except (ValueError, TypeError):
        return False


def create_account(
    store: dict[str, str],
    username: str,
    password: str,
) -> bool:
    if username in store:
        return False

    record = _hash_password(password)
    store[username] = record
    return True


def reset_password(
    store: dict[str, str],
    username: str,
    new_password: str,
    authorized: bool,
) -> bool:
    if not authorized or username not in store:
        return False

    record = _hash_password(new_password)
    store[username] = record
    return True


def login(
    store: dict[str, str],
    username: str,
    password: str,
) -> bool:
    record = store.get(username)

    if record is None:
        return False

    return _verify_password(record, password)
