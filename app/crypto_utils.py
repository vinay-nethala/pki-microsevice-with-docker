# app/crypto_utils.py
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding, rsa
import base64

def load_private_key(path: str):
    with open(path, "rb") as f:
        return serialization.load_pem_private_key(f.read(), password=None)

def load_public_key(path: str):
    with open(path, "rb") as f:
        return serialization.load_pem_public_key(f.read())

def decrypt_seed(encrypted_seed_b64: str, private_key) -> str:
    ct = base64.b64decode(encrypted_seed_b64)
    plain = private_key.decrypt(
        ct,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    s = plain.decode("utf-8").strip()
    # validate 64 hex chars
    if len(s) != 64 or any(c not in "0123456789abcdef" for c in s.lower()):
        raise ValueError("Decrypted seed is invalid")
    return s.lower()

def sign_commit_hash(commit_hash_hex: str, private_key) -> bytes:
    # input commit_hash_hex is hex string
    data = bytes.fromhex(commit_hash_hex)
    signature = private_key.sign(
        data,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )
    return signature

def encrypt_with_instructor_pub(signature: bytes, instructor_pubkey) -> bytes:
    ct = instructor_pubkey.encrypt(
        signature,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return ct
