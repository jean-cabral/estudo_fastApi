from argon2 import PasswordHasher

class Hash():
    def encrypt(password: str):
        ph = PasswordHasher()
        hashed = ph.hash(password)

        return hashed