from passlib.context import CryptContext


password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str):
    return password_context.hash(password)


def verify_password(passwd_payload: str, passwd_db: str):
    return password_context.verify(passwd_payload, passwd_db)