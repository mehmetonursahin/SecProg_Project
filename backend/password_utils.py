import hashlib
import secrets

def generate_salt(length=16):
    """Generate a random hex salt."""
    return secrets.token_hex(length)

def hash_password(password, salt):
    """Hash a password with the provided salt using SHA-256."""
    if isinstance(salt, bytes):
        salt = salt.decode('utf-8')
    if isinstance(password, bytes):
        password = password.decode('utf-8')

    salted_password = (salt + password).encode('utf-8')
    hashed = hashlib.sha256(salted_password).hexdigest()
    return hashed

