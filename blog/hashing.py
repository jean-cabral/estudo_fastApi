from argon2 import PasswordHasher


class Hash():
    def encrypt(password: str):
        ph = PasswordHasher()
        hashed = ph.hash(password)

        return hashed


    def verify(hashed_password, plain_password):
        ph = PasswordHasher()
        verificacao = ph.verify(hashed_password, plain_password)
        return verificacao