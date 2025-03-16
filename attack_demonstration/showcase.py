# Austin Doucette
# CPSC 418 - Project
# March 2025

from Crypto.Cipher import ChaCha20
import secrets
import time

from encrypt import LCG, generate_key, encrypt
from attack import brute_force


def example(plaintext: str, bits: int = 256):
    """
    Example showcasing LCG weakness.

    Args:
        message (str): Message to be encrypted
        bits (int): Range of LCG initial seeding. 1 <= bits <= 32

    """
    KEY_LENGTH = 256
    NONCE_LENGTH = 64

    lcg = LCG()
    lcg.srand(secrets.randbits(bits))       # Seed the lcg

    key = generate_key(lcg, KEY_LENGTH)                         # Generate the key using the lcg
    nonce = secrets.randbits(NONCE_LENGTH).to_bytes(8, "big")   # Generate a random nonce
    ciphertext = encrypt(plaintext, key, nonce)
    constants = {"plaintext": plaintext.encode(), "ciphertext": ciphertext, "nonce": nonce}

    start_time = time.time()
    found_seed = hex(brute_force(constants, 7))     # Perform brute force
    end_time = time.time()
    run_time = end_time - start_time

    lcg.srand(found_seed)                           # Decrypt with found key
    found_key = generate_key(lcg, KEY_LENGTH)
    cipher = ChaCha20.new(key=found_key, nonce=nonce)
    decrypted_ciphertext = cipher.decrypt(ciphertext).decode()

    print("Results:\n")
    print(f"True Values: \n Plaintext: {plaintext} \n Key: {key.hex()} Ciphertext: {ciphertext.hex()} \n")
    print(f"Found Values: \n Plaintext: {decrypted_ciphertext} \n Key: {found_key.hex()} \n Runtime: {run_time}")


if __name__ == "__main__":
    example("Hello There!!!")