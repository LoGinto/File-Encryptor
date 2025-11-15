# Decrypt.py

import os
import zipfile
from cryptography.hazmat.primitives.ciphers.aead import AESGCM


def decrypt_file(enc_path, key_path):
    # 1. Validate paths
    if not os.path.isfile(enc_path):
        print("Encrypted file not found!")
        return

    if not os.path.isfile(key_path):
        print("Key file not found!")
        return

    print("Files found. Loading key and encrypted data...")

    # 2. Load key + encrypted data
    with open(key_path, "rb") as kf:
        key = kf.read()

    with open(enc_path, "rb") as ef:
        encrypted_data = ef.read()

    # 3. Extract nonce + ciphertext
    nonce = encrypted_data[:12]
    ciphertext = encrypted_data[12:]

    # 4. Decrypt
    aes = AESGCM(key)
    try:
        plaintext = aes.decrypt(nonce, ciphertext, None)
    except Exception:
        print("Decryption failed! Wrong key or corrupted file.")
        return

    print("Decryption successful. Saving file...")

    # 5. Determine output filename (remove .enc)
    if enc_path.endswith(".enc"):
        out_path = enc_path[:-4]
    else:
        out_path = enc_path + ".decrypted"

    # 6. Save decrypted file
    with open(out_path, "wb") as f:
        f.write(plaintext)

    print(f"Decrypted file saved as: {out_path}")

    # 7. Auto-unzip if it's a ZIP
    if out_path.lower().endswith(".zip"):
        print("Decrypted file is a ZIP. Extracting...")

        extract_folder = out_path[:-4]  # remove .zip

        try:
            with zipfile.ZipFile(out_path, 'r') as zip_ref:
                zip_ref.extractall(extract_folder)
            print(f"ZIP extracted to: {extract_folder}")
        except Exception as e:
            print("Failed to unzip:", e)
            # we still keep the .zip file and return

        # Ask whether to delete the ZIP
        delete_zip = input("Delete the decrypted ZIP file? (y/n): ").lower()
        if delete_zip == "y":
            try:
                os.remove(out_path)
                print("ZIP file deleted.")
            except Exception:
                print("Failed to delete the ZIP file.")
        else:
            print("ZIP file kept.")

    # 8. Ask whether to delete the encrypted .enc file
    delete_choice = input("Delete the encrypted file? (y/n): ").lower()

    if delete_choice == "y":
        try:
            os.remove(enc_path)
            print("Encrypted file deleted.")
        except Exception:
            print("Failed to delete encrypted file.")
    else:
        print("Encrypted file kept.")
