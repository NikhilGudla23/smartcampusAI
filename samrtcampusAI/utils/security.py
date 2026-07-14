import hashlib
import re

def hash_password(password: str) -> str:
    """Hash a password using SHA-256 with a secure static salt."""
    salt = "smartcampusai_secure_salt_998877"
    hashed = hashlib.sha256((salt + password).encode('utf-8')).hexdigest()
    return f"sha256${hashed}"

def verify_password(password: str, hashed_password: str) -> bool:
    """Verify password by checking its hash against stored hash."""
    return hash_password(password) == hashed_password

def validate_email(email: str) -> bool:
    """Validate email using regex."""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

def validate_password_strength(password: str) -> tuple[bool, str]:
    """Validate password strength (length, numbers, uppercase)."""
    if len(password) < 6:
        return False, "Password must be at least 6 characters long."
    if not any(char.isdigit() for char in password):
        return False, "Password must contain at least one number."
    if not any(char.isupper() for char in password):
        return False, "Password must contain at least one uppercase letter."
    return True, ""
