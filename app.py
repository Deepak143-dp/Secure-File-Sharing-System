from flask import Flask, render_template, request, send_file, redirect, url_for, flash
import os
from hashlib import sha256

from crypto_utils import encrypt_file, decrypt_file
from config import UPLOAD_FOLDER, DECRYPT_FOLDER

app = Flask(__name__)
app.secret_key = "supersecretflaskkey"


@app.route("/")
def index():
    files = os.listdir(UPLOAD_FOLDER)
    return render_template("upload.html", files=files)


# 🔐 ENCRYPT FILE (ASK PASSWORD)
@app.route("/encrypt", methods=["POST"])
def encrypt():
    file = request.files.get("file")
    password = request.form.get("password")

    if not file or not password:
        flash("File and encryption key required")
        return redirect(url_for("index"))

    data = file.read()

    # 🔑 derive AES key from user password
    key = sha256(password.encode()).digest()

    encrypted_data = encrypt_file(data, key)

    encrypted_filename = file.filename + ".enc"
    encrypted_path = os.path.join(UPLOAD_FOLDER, encrypted_filename)

    with open(encrypted_path, "wb") as f:
        f.write(encrypted_data)

    flash("✅ File encrypted and stored successfully!")
    return redirect(url_for("index"))


# 🔓 DECRYPT FILE (ASK PASSWORD)
@app.route("/decrypt", methods=["POST"])
def decrypt():
    filename = request.form.get("filename")
    password = request.form.get("password")

    if not filename or not password:
        flash("Filename and decryption key required")
        return redirect(url_for("index"))

    encrypted_path = os.path.join(UPLOAD_FOLDER, filename)

    if not os.path.exists(encrypted_path):
        flash("Encrypted file not found")
        return redirect(url_for("index"))

    key = sha256(password.encode()).digest()

    try:
        with open(encrypted_path, "rb") as f:
            encrypted_data = f.read()

        decrypted_data = decrypt_file(encrypted_data, key)

        output_filename = filename.replace(".enc", "")
        output_path = os.path.join(DECRYPT_FOLDER, output_filename)

        with open(output_path, "wb") as f:
            f.write(decrypted_data)

        return send_file(output_path, as_attachment=True)

    except Exception:
        flash("❌ Wrong key! Decryption failed.")
        return redirect(url_for("index"))


# 🔐 DOWNLOAD ENCRYPTED FILE ONLY
@app.route("/download/encrypted/<filename>")
def download_encrypted(filename):
    encrypted_path = os.path.join(UPLOAD_FOLDER, filename)

    if not os.path.exists(encrypted_path):
        flash("Encrypted file not found")
        return redirect(url_for("index"))

    return send_file(encrypted_path, as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)
