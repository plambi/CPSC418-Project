# Austin Doucette
# CPSC 418 - Project
# March 2025

from Crypto.Cipher import ChaCha20
import secrets
import time

from encrypt import LCG, generate_key, encrypt
from attack_multi import brute_force



def example(plaintext: str, bits: int = 32, cpu_count: int = None):
    """
    Example showcasing LCG weakness.

    Args:
        message (str): Message to be encrypted
        bits (int): Range of LCG initial seeding (in bits). Defaults to 32.

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
    results = brute_force(constants=constants, processes=cpu_count, max_key_length=bits)     # Perform brute force
    end_time = time.time()
    run_time = end_time - start_time

    if not results:
        print("Key not found.")
        return

    found_seed = results[0]
    lcg.srand(found_seed)                           # Decrypt with found key
    found_key = generate_key(lcg, KEY_LENGTH)
    cipher = ChaCha20.new(key=found_key, nonce=nonce)
    decrypted_ciphertext = cipher.decrypt(ciphertext).decode()

    print("Results:\n")
    print(f"True Values: \n\tPlaintext: {plaintext} \n\tKey: {key.hex()} \n \tCiphertext: {ciphertext.hex()} \n")
    print(f"Found Values: \n\tPlaintext: {decrypted_ciphertext} \n\tKey: {found_key.hex()} \n\tRuntime: {run_time}")



if __name__ == "__main__":
    """ 
        Run the simulation here!
    """
    message = "Hello There"         # Any message should work
    lcg_range = 12                  # The range of the intial LCG seed. Its maximum is 2^32 and that would be used in practice. But for testing faster set anything you like
    max_cores = 7                   # The number of CPU cores the simulation will use. If None it uses all cores. 
    example(message, lcg_range, max_cores)