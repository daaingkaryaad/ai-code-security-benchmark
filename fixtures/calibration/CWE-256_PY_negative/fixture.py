import hashlib
import secrets

def register(store, username, password):
    salt = secrets.token_bytes(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, 600000)
    store[username] = salt.hex() + ":" + digest.hex()
