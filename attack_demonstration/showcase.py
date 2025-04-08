# Group 7 - Austin Doucette
# CPSC 418 - Explorations of Pseudo Random Number Generation
# April 2025

from Crypto.Cipher import ChaCha20
import secrets
import time

from encrypt import LCG, generate_key, encrypt
from attack import brute_force


def example(plaintext: str, seed_bits: int = 32, thread_count: int = None):
    """
    Example showcasing how 256 bit keys generated with the C rand function (Linear Congruential Generation) is insecure against known plaintext attacks.

    Args:
        plaintext (str): The known plaintext
        seed_bits (int): rand supports seeds up to 2^31 but for testing purposes you can limit it to a different power of 2
        thread_count (int): Number of threads to be used during brute forcing. Reccommended is CPU count.
    
    """
    KEY_LENGTH = 256
    NONCE_LENGTH = 64

    lcg = LCG()
    lcg.srand(secrets.randbits(seed_bits))       # Seed the lcg

    # Victim: Generate a key using the LCG and encrypt the message with it
    key = generate_key(lcg, KEY_LENGTH)                         # Generate the key using the lcg
    nonce = secrets.randbits(NONCE_LENGTH).to_bytes(8, "big")   # Generate a random nonce
    ciphertext = encrypt(plaintext, key, nonce)

    # Attacker: Use the known plaintext, ciphertext, and nonce to derive the initial seeding of the LCG
    constants = {"plaintext": plaintext.encode(), "ciphertext": ciphertext, "nonce": nonce}
    start_time = time.time()
    found_seed = brute_force(constants=constants, thread_count=thread_count, max_key_length=seed_bits)     # Perform brute force
    end_time = time.time()
    run_time = end_time - start_time

    # Attacker: Generate the key using the found seed
    lcg.srand(found_seed)
    found_key = generate_key(lcg, KEY_LENGTH)
    cipher = ChaCha20.new(key=found_key, nonce=nonce)
    decrypted_ciphertext = cipher.decrypt(ciphertext).decode()

    print(f"True Values: \n\tPlaintext: {plaintext} \n\tKey: {key.hex()} \n \tCiphertext: {ciphertext.hex()} \n")
    print(f"Found Values: \n\tPlaintext: {decrypted_ciphertext} \n\tKey: {found_key.hex()} \n\tRuntime: {round(run_time, 2)} seconds \n\tSeeds Tried: {found_seed}")


if __name__ == "__main__":
    message = "Hello There"         # Any message works
    lcg_range = 24                  # The range of the intial LCG seed. Its maximum is 2^31 and that would be used in practice. But for testing faster set anything you like
    max_cores = 4                   # The number of threads the simulation will create. Use your computers core count. I would reccommend 4 if you don't know.
    example(message, lcg_range, max_cores)
