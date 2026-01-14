import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
DECRYPT_FOLDER = os.path.join(BASE_DIR, "decrypted")

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(DECRYPT_FOLDER, exist_ok=True)
