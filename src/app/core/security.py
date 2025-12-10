from bcrypt import gensalt, hashpw
from pydantic import BaseModel


class Password(BaseModel):
    hashed_password: str
    salt: str


def hash_password(text: str) -> Password:
    bytes = text.encode("utf-8")
    salt = gensalt()
    hash = hashpw(bytes, salt)

    return Password(hashed_password=hash.decode(), salt=salt.decode())
