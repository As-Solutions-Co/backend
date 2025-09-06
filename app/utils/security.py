import bcrypt


def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    password_bytes = password.encode()
    hashed_password = bcrypt.hashpw(password_bytes, salt)
    return hashed_password.decode()
