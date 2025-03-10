import secrets

# Generate a 64-byte secret key
SECRET_KEY = secrets.token_hex(32)  # 32 bytes = 64 hex characters
print(SECRET_KEY)
