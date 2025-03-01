import json
import os
from dotenv import load_dotenv
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import padding as asym_padding
from cryptography.hazmat.primitives.hashes import SHA256
from cryptography.hazmat.primitives.serialization import load_pem_private_key
from base64 import b64decode, b64encode

load_dotenv()

PRIVATE_KEY = os.environ['PRIVATE_KEY']

class FlowEndpointException(Exception):
    def __init__(self, status_code, message):
        super().__init__(message)
        self.status_code = status_code


def decrypt_request(body, private_pem, passphrase):
    encrypted_aes_key = body["encrypted_aes_key"]
    encrypted_flow_data = body["encrypted_flow_data"]
    initial_vector = body["initial_vector"]

    private_key = load_pem_private_key(private_pem.encode(), password=passphrase.encode(), backend=default_backend())

    try:
        decrypted_aes_key = private_key.decrypt(
            b64decode(encrypted_aes_key),
            asym_padding.OAEP(
                mgf=asym_padding.MGF1(algorithm=SHA256()),
                algorithm=SHA256(),
                label=None
            )
        )
    except Exception as error:
        print(error)
        raise FlowEndpointException(421, "Failed to decrypt the request. Please verify your private key.")

    flow_data_buffer = b64decode(encrypted_flow_data)
    initial_vector_buffer = b64decode(initial_vector)

    TAG_LENGTH = 16
    encrypted_flow_data_body = flow_data_buffer[:-TAG_LENGTH]
    encrypted_flow_data_tag = flow_data_buffer[-TAG_LENGTH:]

    decryptor = Cipher(
        algorithms.AES(decrypted_aes_key),
        modes.GCM(initial_vector_buffer, encrypted_flow_data_tag),
        backend=default_backend()
    ).decryptor()

    try:
        decrypted_data = decryptor.update(encrypted_flow_data_body) + decryptor.finalize()
    except Exception as error:
        print(error)
        raise FlowEndpointException(422, "Failed to decrypt flow data.")

    return {
        "decryptedBody": json.loads(decrypted_data.decode("utf-8")),
        "aesKeyBuffer": decrypted_aes_key,
        "initialVectorBuffer": initial_vector_buffer
    }


def encrypt_response(response, aes_key_buffer, initial_vector_buffer):
    flipped_iv = bytearray(~b & 0xFF for b in initial_vector_buffer)

    encryptor = Cipher(
        algorithms.AES(aes_key_buffer),
        modes.GCM(bytes(flipped_iv)),
        backend=default_backend()
    ).encryptor()

    encrypted_response = encryptor.update(json.dumps(response).encode("utf-8")) + encryptor.finalize()

    return b64encode(encrypted_response + encryptor.tag).decode("utf-8")