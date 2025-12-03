# app/totp_utils.py
import pyotp
import base64
import time

def hex_to_base32(hex_seed: str) -> str:
    seed_bytes = bytes.fromhex(hex_seed)
    return base64.b32encode(seed_bytes).decode('utf-8')

def generate_totp_code(hex_seed: str) -> dict:
    base32_seed = hex_to_base32(hex_seed)
    totp = pyotp.TOTP(base32_seed, digits=6, interval=30)
    code = totp.now()
    remaining = 30 - (int(time.time()) % 30)
    return {"code": code, "valid_for": remaining}

def verify_totp_code(hex_seed: str, code: str) -> bool:
    base32_seed = hex_to_base32(hex_seed)
    totp = pyotp.TOTP(base32_seed, digits=6, interval=30)
    return totp.verify(code, valid_window=1)
