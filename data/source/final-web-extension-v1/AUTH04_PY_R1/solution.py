
import hashlib
import hmac
import secrets


_ITERATIONS = 600_000
_SALT_SIZE = 16


def activate_account(
    store: dict[str, str],
    username: str,
    password: str,
    invitation_accepted: bool
) -> bool:
    if not invitation_accepted or username in store:
        return False

    salt = secrets.token_bytes(_SALT_SIZE)
    password_hash = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt,
        _ITERATIONS
    )

    store[username] = (
        f"pbkdf2_sha256${_ITERATIONS}$"
        f"{salt.hex()}${password_hash.hex()}"
    )
    return True


def login(
    store: dict[str, str],
    username: str,
    password: str
) -> bool:
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
        expected_hash = bytes.fromhex(expected_hex)

        actual_hash = hashlib.pbkdf2_hmac(
            "sha256",
            password.encode("utf-8"),
            salt,
            iterations,
            dklen=len(expected_hash)
        )

        return hmac.compare_digest(actual_hash, expected_hash)

    except (ValueError, TypeError, OverflowError):
        return False
