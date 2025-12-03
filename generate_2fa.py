import base64
import pyotp
import datetime

def generate_2fa_from_decrypted_file(file_path):
    # Open the decrypted file (binary mode)
    with open(file_path, "rb") as f:
        decrypted_bytes = f.read()

    # Convert binary data to base32 (needed for 2FA)
    base32_seed = base64.b32encode(decrypted_bytes).decode('utf-8')

    # Generate 2FA code using pyotp
    totp = pyotp.TOTP(base32_seed)
    code = totp.now()

    # Print the current 2FA code
    now_utc = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
    print(f"{now_utc} - Your 2FA Code: {code}")

# Change the file name here if yours is different
generate_2fa_from_decrypted_file("decrypted_seed.bin.txt")