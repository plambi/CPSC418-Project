# Austin Doucette
# CPSC 418 - Project
# March 2025

from Crypto.Cipher import ChaCha20
import secrets  # Used to seed LCG



class LCG:
    def __init__(self, multiplier: int = 1103515245, increment: int = 12345, modulus: int = 2147483648, seed: int = 0):
        """ Initializes an LCG. Defaults to values used in the C rand function. """
        self.multiplier = multiplier
        self.increment = increment
        self.modulus = modulus
        self.state = seed

    def srand(self, seed: int):
        """ Seed the LCG """
        self.state = seed

    def rand(self):
        self.state = ((self.multiplier * self.state) + self.increment) % self.modulus
        return self.state
    
    def get_modulus(self):
        return self.modulus



def encrypt(message: str, key: bytes, nonce: bytes):
    """ 
    Encrypts a message using ChaCha20

    Args:
        message (string): Plaintext
        key (bytes): 256 bit key
        nonce (bytes): 64 bit nonce

    Returns:
        bytes: Ciphertext
    
    """
    cipher = ChaCha20.new(key=key, nonce=nonce)
    ciphertext = cipher.encrypt(message.encode())
    return ciphertext



def generate_key(lcg: LCG, length: int):
    """
    Uses the LCG to generate a bitstring.

    Args:
        lcg (LCG): LCG object. Must be seeded beforehand.
        length (int): Number of bits in key. Must be a multiple of the lcg modulus.

    Returns:
        bytes: Key

    """
    keys = []
    lcg_output_length = lcg.get_modulus().bit_length()

    if(length % lcg_output_length != 0):
        print("Error improper use of generate_key() / length must be a multiple of the LCG modulus.")
        return -1
    
    for _ in range(int(length / lcg_output_length)):
        keys.append(lcg.rand().to_bytes(int(lcg_output_length / 8), "big"))

    result = b''
    for i in range(int(length / lcg_output_length)):
        result += keys[i]

    return result
