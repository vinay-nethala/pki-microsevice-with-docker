import base64
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding

# read commit hash
with open("commit_hash.txt", "rb") as f:
    commit_hash = f.read().strip()

# load private key
with open("student_private.pem", "rb") as key_file:
    private_key = serialization.load_pem_private_key(
        key_file.read(),
        password=None
    )

# sign commit hash
signature = private_key.sign(
    commit_hash,
    padding.PSS(
        mgf=padding.MGF1(hashes.SHA256()),
        salt_length=32
    ),
    hashes.SHA256()
)

# save as base64
with open("commit_signature.b64", "wb") as f:
    f.write(base64.b64encode(signature))

print("Signature generated successfully!")