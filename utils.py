from passlib.context import CryptContext
import hashlib

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    """Hash a plain text password"""
    # Pre-hash with SHA256 to handle long passwords and then use bcrypt
    # This ensures we stay within bcrypt's 72-byte limit
    password_bytes = password.encode('utf-8')
    sha256_hash = hashlib.sha256(password_bytes).hexdigest()
    return pwd_context.hash(sha256_hash)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain text password against a hashed password"""
    # Pre-hash the plain password with SHA256 before verifying
    password_bytes = plain_password.encode('utf-8')
    sha256_hash = hashlib.sha256(password_bytes).hexdigest()
    return pwd_context.verify(sha256_hash, hashed_password)
