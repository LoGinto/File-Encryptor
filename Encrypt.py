# Encrypt.py

import os
import shutil
from cryptography.hazmat.primitives.ciphers.aead import AESGCM


def encrypt_file(path):
    # 1. If it's a folder, zip it first
    if os.path.isdir(path):
        print("Folder detected. Creating ZIP...")
        zip_path = path.rstrip("/\\") + ".zip"
        shutil.make_archive(path, 'zip', path)   # creates <path>.zip
        path = zip_path
        print(f"ZIP created: {zip_path}")

    # 2. Validate file exists
    if not os.path.isfile(path):
        print("File not found!")
        return

    # 3. Read file contents
    with open(path, "rb") as f:
        data = f.read()

    # 4. AES-256-GCM encryption
    key = AESGCM.generate_key(bit_length=256)
    aes = AESGCM(key)
    nonce = os.urandom(12)
    ciphertext = aes.encrypt(nonce, data, None)

    # 5. Save encrypted file: <path>.enc
    enc_path = path + ".enc"
    with open(enc_path, "wb") as f:
        f.write(nonce + ciphertext)

    print(f"Encrypted file saved as: {enc_path}")

    # 6. Ask WHERE to save the key for THIS encrypted file
    while True:
        key_dest = input(
            "Enter path to save the encryption key (file or folder, "
            "or press Enter to skip): "
        ).strip()

        # allow user to skip (dangerous but your choice)
        if key_dest == "":
            print("Key was NOT saved. WARNING: without this key, you cannot decrypt.")
            break

        # If user gave an existing folder or ended with / or \, create a default key file name in it
        if os.path.isdir(key_dest) or key_dest.endswith(os.sep):
            base_name = os.path.basename(enc_path)  # e.g. "password.txt.enc"
            key_filename = base_name + ".key"       # e.g. "password.txt.enc.key"
            key_path = os.path.join(key_dest, key_filename)
        else:
            # Assume it's a full file path
            key_path = key_dest

        # Ensure parent directory exists (if specified)
        parent_dir = os.path.dirname(key_path)
        if parent_dir and not os.path.isdir(parent_dir):
            print("Folder does not exist. Please enter an existing folder or full file path.")
            continue

        try:
            with open(key_path, "wb") as f:
                f.write(key)
            print(f"Key saved to: {key_path}")
            break
        except Exception as e:
            print(f"Failed to save key: {e}")
            print("Try a different path.")

    # 7. Ask whether to delete the original (plaintext) file/zip
    delete_choice = input("Delete the original (unencrypted) file? (y/n): ").lower()
    if delete_choice == "y":
        try:
            os.remove(path)
            print("Original file deleted.")
        except Exception:
            print("Failed to delete the original file.")
    else:
        print("Original file kept.")
