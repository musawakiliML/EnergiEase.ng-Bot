import sys

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa

if len(sys.argv) < 2:
    raise ValueError(
        "Passphrase is empty. Please include a passphrase argument to generate the keys like: python key_generator.py {passphrase}"
    )

passphrase = sys.argv[1].encode("utf-8")

try:
    # Generate RSA Key Pair
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
    )

    # Serialize private key with passphrase
    private_key_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.BestAvailableEncryption(passphrase),
    )

    # Serialize public key
    public_key = private_key.public_key()
    public_key_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )

    print(
        "Successfully created your public-private key pair. Please copy the below values into your .env file\n"
    )
    print(
        "************* COPY PASSPHRASE & PRIVATE KEY BELOW TO .env FILE *************"
    )
    print(f"PASSPHRASE=\"{passphrase.decode('utf-8')}\"\n")
    print(f"PRIVATE_KEY=\"{private_key_pem.decode('utf-8')}\"\n")
    print(
        "************* COPY PASSPHRASE & PRIVATE KEY ABOVE TO .env FILE *************\n"
    )
    print("************* COPY PUBLIC KEY BELOW *************")
    print(public_key_pem.decode("utf-8"))
    print("************* COPY PUBLIC KEY ABOVE *************")

except Exception as e:
    print("Error while creating public-private key pair:", e)
