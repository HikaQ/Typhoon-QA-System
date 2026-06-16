from werkzeug.security import generate_password_hash, check_password_hash

def hash_password(password: str) -> str:
    # Use pbkdf2 for better compatibility with legacy VARCHAR(128) columns.
    return generate_password_hash(password, method="pbkdf2:sha256:600000")

def verify_password(password: str, password_hash: str) -> bool:
    return check_password_hash(password_hash, password)
