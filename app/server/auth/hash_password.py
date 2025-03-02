import bcrypt

# Create Hash function


class HashPassword:
    def create_hash(self, password: str):
        password_bytes = password.encode("utf-8")
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password=password_bytes, salt=salt)
        return hashed_password

    def verify_hash(self, plain_password: str, hash_password):
        password_byte_enc = plain_password.encode("utf-8")
        return bcrypt.checkpw(password=password_byte_enc, hashed_password=hash_password)
