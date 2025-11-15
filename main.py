# main.py

import os
from Encrypt import encrypt_file
from Decrypt import decrypt_file


def main():
    while True:
        print("\n=== File Encryptor ===")
        print("1. Encrypt")
        print("2. Decrypt")
        print("3. Exit")

        choice = input("Select an option: ").strip()

        # -----------------------------
        # Encrypt
        # -----------------------------
        if choice == "1":
            while True:
                path = input(
                    "Enter the path to the file or folder to encrypt "
                    "(or press Enter to cancel): "
                ).strip()

                if path == "":
                    # Back to menu
                    break

                if not os.path.exists(path):
                    print("Path not found. Try again.")
                    continue

                # Call encrypt function
                encrypt_file(path)
                break

        # -----------------------------
        # Decrypt
        # -----------------------------
        elif choice == "2":
            while True:
                enc_path = input(
                    "Enter the path to the encrypted .enc file "
                    "(or press Enter to cancel): "
                ).strip()

                if enc_path == "":
                    break

                if not os.path.isfile(enc_path):
                    print("Encrypted file not found. Try again.")
                    continue

                key_path = input(
                    "Enter the FULL path to the key file "
                    "(or press Enter to cancel): "
                ).strip()

                if key_path == "":
                    break

                if not os.path.isfile(key_path):
                    print("Key file not found. Try again.")
                    continue

                # Call decrypt function
                decrypt_file(enc_path, key_path)
                break

        # -----------------------------
        # Exit
        # -----------------------------
        elif choice == "3":
            print("Goodbye!")
            break

        else:
            print("Invalid option. Try again.")


if __name__ == "__main__":
    main()
