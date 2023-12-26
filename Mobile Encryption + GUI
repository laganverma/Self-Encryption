from tkinter import Tk, Button, Label, PhotoImage
from tkinter import filedialog, messagebox, simpledialog
import tkinter as tk
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.ciphers import Cipher, modes, algorithms
from cryptography.hazmat.primitives.asymmetric import rsa
import os
import time
import hashlib

# Define file_path, aes_key, and encrypted_text as global variables
file_path = None
aes_key = None
encrypted_text = None

# Create a basic blockchain as a list
blockchain = []


# Generate or load the user's RSA key pair
def generate_key_pair():
    private_key_path = "private_key.pem"
    public_key_path = "public_key.pem"

    # Check if public key exists, if not, generate both private and public keys
    if not os.path.exists(public_key_path):
        private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
        public_key = private_key.public_key()

        # Serialize and save the public key to a file
        with open(public_key_path, "wb") as public_key_file:
            public_key_file.write(
                public_key.public_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PublicFormat.SubjectPublicKeyInfo
                )
            )

        # Serialize and save the private key to a file
        with open(private_key_path, "wb") as private_key_file:
            private_key_file.write(
                private_key.private_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PrivateFormat.PKCS8,
                    encryption_algorithm=serialization.NoEncryption()
                )
            )

        return private_key, public_key
    else:
        # Load existing keys from files
        with open(private_key_path, 'rb') as private_key_file:
            private_key = serialization.load_pem_private_key(private_key_file.read(), password=None)

        with open(public_key_path, 'rb') as public_key_file:
            public_key = serialization.load_pem_public_key(public_key_file.read())

        return private_key, public_key


# Encrypt a file using AES in chunks and compute SHA hash for each chunk
def encrypt_file_in_chunks(file_path, key):
    chunk_size = 1024  # You can adjust the chunk size based on your needs

    with open(file_path, 'rb') as file:
        sha_hash = hashlib.sha256()
        encrypted_chunks = []

        chunk = file.read(chunk_size)
        while chunk:
            cipher = Cipher(algorithms.AES(key), modes.CFB(b'\x00' * 16))
            encryptor = cipher.encryptor()
            encrypted_chunk = encryptor.update(chunk) + encryptor.finalize()

            # Print the encrypted chunk
            print("Encrypted Chunk:", encrypted_chunk)

            # Compute SHA hash of the encrypted chunk
            sha_hash.update(encrypted_chunk)

            encrypted_chunks.append(encrypted_chunk)
            chunk = file.read(chunk_size)

    return b''.join(encrypted_chunks), sha_hash.hexdigest()


# Decrypt a file using AES in chunks
def decrypt_file_in_chunks(encrypted_text, key):
    chunk_size = 1024

    cipher = Cipher(algorithms.AES(key), modes.CFB(b'\x00' * 16))
    decryptor = cipher.decryptor()

    decrypted_chunks = []
    for i in range(0, len(encrypted_text), chunk_size):
        chunk = encrypted_text[i:i+chunk_size]
        decrypted_chunk = decryptor.update(chunk) + decryptor.finalize()

        # Print the decrypted chunk
        print("Decrypted Chunk:", decrypted_chunk)

        decrypted_chunks.append(decrypted_chunk)

    return b''.join(decrypted_chunks)


# Save the encrypted text to a file
def save_encrypted_file(encrypted_text, file_path):
    with open(file_path, 'wb') as file:
        file.write(encrypted_text)


# Load the user's public key from a file
def load_public_key(file_path):
    with open(file_path, 'rb') as key_file:
        public_key = serialization.load_pem_public_key(key_file.read())
    return public_key


# Record a transaction in the blockchain
def record_transaction(user, action, file_path, sha_hash=None):
    transaction = {
        "user": user,
        "action": action,
        "file_path": file_path,
        "sha_hash": sha_hash  # Include the SHA hash in the transaction record
    }
    blockchain.append(transaction)


# GUI setup
class SelfEncryptionApp:
    def __init__(self, master):
        self.master = master
        master.title("Mobile-Self Encryption")

        # Load images
        self.logo = PhotoImage(file=r"C:\Users\Lagan\Desktop\download.png")

        # Create GUI buttons for file selection, encryption, decryption, and showing the blockchain
        self.logo_label = Label(master, image=self.logo)
        self.logo_label.grid(row=0, column=0, columnspan=2, pady=10)

        self.select_button = Button(master, text="Select File", command=self.select_file, width=20)
        self.select_button.grid(row=1, column=0, pady=10)

        self.encrypt_button = Button(master, text="Encrypt and Replace", command=self.encrypt_and_replace, width=20)
        self.encrypt_button.grid(row=2, column=0, pady=10)

        self.decrypt_button = Button(master, text="Decrypt", command=self.decrypt, width=20)
        self.decrypt_button.grid(row=3, column=0, pady=10)

        self.show_blockchain_button = Button(master, text="Show Blockchain", command=self.show_blockchain, width=20)
        self.show_blockchain_button.grid(row=4, column=0, pady=10)

    def select_file(self):
        global file_path  # Use the global file_path variable
        file_path = filedialog.askopenfilename()
        if file_path:
            messagebox.showinfo("File Selected", f"Selected file: {file_path}")

    def encrypt_and_replace(self):
        global file_path, aes_key, encrypted_text  # Use the global variables

        if file_path:
            # Check if the AES key is already generated
            if aes_key is None:
                # Generate or load user's RSA public key
                private_key, public_key = generate_key_pair()

                if public_key:
                    # Generate a new AES key for encryption
                    aes_key = os.urandom(32)  # Replace this with a securely generated key
                else:
                    messagebox.showerror("Error", "Public key not found or generated.")
                    return

            # Encrypt the selected file using AES and compute SHA hash
            encrypted_text, sha_hash = encrypt_file_in_chunks(file_path, aes_key)

            # Replace the original file with the encrypted file
            save_encrypted_file(encrypted_text, file_path)

            # Record the encryption transaction in the blockchain with SHA hash
            record_transaction("Encryption", "Encryption", file_path, sha_hash)
            messagebox.showinfo("Encryption", "File encrypted successfully.")
        else:
            messagebox.showwarning("Warning", "Please select a file first.")

    def decrypt(self):
        global file_path, aes_key, encrypted_text  # Use the global variables

        if file_path and aes_key and encrypted_text:
            # Prompt for the username and password
            username = simple_dialog("Authentication", "Enter your username:")
            password = simple_dialog("Authentication", "Enter your password:")

            if authenticate(username, password):
                # Load the user's private RSA key
                with open("private_key.pem", 'rb') as key_file:
                    # Do not provide a password if the key is not encrypted
                    private_key = serialization.load_pem_private_key(key_file.read(), password=None)

                # Decrypt the file using the AES key
                decrypted_text = decrypt_file_in_chunks(encrypted_text, aes_key)

                # Compute SHA hash of the decrypted text
                sha_hash_decrypted = hashlib.sha256(decrypted_text).hexdigest()

                # Display decrypted content in hexadecimal format
                decrypted_hex = decrypted_text.hex()
                print("Decrypted Content (Hexadecimal):", decrypted_hex)

                # Record the decryption transaction in the blockchain with SHA hash
                timestamp = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())
                decrypted_file_path = f"decrypted_file_{timestamp}.txt"  # Unique file name with timestamp
                with open(decrypted_file_path, 'wb') as decrypted_file:
                    decrypted_file.write(decrypted_text)

                print(f"Decrypted content saved to {decrypted_file_path}")
                record_transaction(username, "Decryption",
                                   decrypted_file_path,
                                   sha_hash_decrypted)  # Record decryption transaction with SHA hash
                messagebox.showinfo("Decryption",
                                    f"File decrypted successfully.\nDecrypted file saved to {decrypted_file_path}")
            else:
                messagebox.showerror("Authentication Failed",
                                     "Authentication failed. Access denied. Please check your username and password.")
        else:
            messagebox.showwarning("Warning", "Please select a file and perform encryption first.")

    def show_blockchain(self):
        if blockchain:
            message = "Blockchain Transactions:\n\n"
            for i, transaction in enumerate(blockchain, start=1):
                message += f"Block {i}:\n"
                message += f"User: {transaction['user']}\n"
                message += f"Action: {transaction['action']}\n"
                message += f"File Path: {transaction['file_path']}\n"
                message += f"SHA Hash: {transaction['sha_hash']}\n\n"  # Include SHA hash in the display
        else:
            message = "Blockchain is empty."
        messagebox.showinfo("Blockchain", message)


def simple_dialog(title, prompt):
    return simpledialog.askstring(title, prompt)


# Define authentication credentials
def authenticate(username, password):
    # You can implement your authentication logic here
    # For simplicity, this example allows any username and password
    return True


# Run the GUI
root = Tk()
app = SelfEncryptionApp(root)
root.mainloop()
