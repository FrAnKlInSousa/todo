from pwdlib import PasswordHash

pwd_context = PasswordHash.recommended()


def create_password_hash(password: str):
    return pwd_context.hash(password=password)


def verify_password(password: str, hashed_password: str):
    return pwd_context.verify(password=password, hash=hashed_password)
