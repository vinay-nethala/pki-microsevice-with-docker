# app/main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pathlib import Path
import os
from app.crypto_utils import load_private_key, decrypt_seed
from app.totp_utils import generate_totp_code, verify_totp_code

# --- Paths ---
# Root folder of the project (parent of 'app')
ROOT_DIR = Path(__file__).parent.parent
DATA_PATH = ROOT_DIR / "data"
SEED_FILE = DATA_PATH / "seed.txt"
STUDENT_PRIVATE_PATH = ROOT_DIR / "student_private.pem"

# --- FastAPI app ---
app = FastAPI()

# --- Request models ---
class DecryptRequest(BaseModel):
    encrypted_seed: str

class VerifyRequest(BaseModel):
    code: str

# --- Load private key once ---
private_key = load_private_key(str(STUDENT_PRIVATE_PATH))

# --- Endpoints ---
@app.post("/decrypt-seed")
async def post_decrypt(req: DecryptRequest):
    try:
        seed_hex = decrypt_seed(req.encrypted_seed, private_key)
        DATA_PATH.mkdir(parents=True, exist_ok=True)
        SEED_FILE.write_text(seed_hex)
        os.chmod(SEED_FILE, 0o600)  # secure the file
        return {"status": "ok"}
    except Exception as e:
        raise HTTPException(status_code=500, detail={"error": "Decryption failed", "detail": str(e)})

@app.get("/generate-2fa")
async def get_generate_2fa():
    if not SEED_FILE.exists():
        raise HTTPException(status_code=500, detail={"error": "Seed not decrypted yet"})
    seed = SEED_FILE.read_text().strip()
    try:
        totp_info = generate_totp_code(seed)
        return totp_info
    except Exception as e:
        raise HTTPException(status_code=500, detail={"error": "TOTP generation failed", "detail": str(e)})

@app.post("/verify-2fa")
async def post_verify_2fa(req: VerifyRequest):
    if not req.code:
        raise HTTPException(status_code=400, detail={"error": "Missing code"})
    if not SEED_FILE.exists():
        raise HTTPException(status_code=500, detail={"error": "Seed not decrypted yet"})
    seed = SEED_FILE.read_text().strip()
    try:
        valid = verify_totp_code(seed, req.code)
        return {"valid": bool(valid)}
    except Exception as e:
        raise HTTPException(status_code=500, detail={"error": "Verification failed", "detail": str(e)})
