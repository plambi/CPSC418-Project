# Austin Doucette
# CPSC 418 - Project
# March 2025

from Crypto.Cipher import ChaCha20
from multiprocessing import Pool, cpu_count

WORKER_CONSTANTS = None

def generate_decryption_key(seed: int):
    """
    Generates a 256 bit key for decryption using the LCG. This can use the LCG object and generate_key() method 
    defined in encrypt.py however for efficiency reasons it wont be used.
    
    Args:
        seed (int): The intial seeding of the LCG

    Returns:
        bytes: Key
    """
    keys = []
    state = ((1103515245 * seed) + 12345) % 2147483648
    keys.append(state.to_bytes(4, "big"))

    for _ in range(1, 8):
        state = ((1103515245 * seed) + 12345) % 2147483648
        keys.append(state.to_bytes(4, "big"))

    result = b''
    for i in range(8):
        result += keys[i]

    return result


def initialize_worker(constants):
    """
    Initialize worker variables.

    Args:
        constants (dict): Dictionary containing "plaintext": bytes, "ciphertext": bytes , "nonce": bytes
    """
    global WORKER_CONSTANTS
    WORKER_CONSTANTS = constants

def try_seed(seed):
    """
    Worker function. Generates a 256 bit key using seed and attempts decryption with it.

    """
    key = generate_decryption_key(seed)
    cipher = ChaCha20.new(key=key, nonce=WORKER_CONSTANTS["nonce"])
    decrypted_ciphertext = cipher.decrypt(WORKER_CONSTANTS["ciphertext"])

    if(decrypted_ciphertext == WORKER_CONSTANTS["plaintext"]):
        return seed
    return None

def brute_force(constants, processes=None):
    """
    Brute forces 32 bit LCG generated key encrypted with ChaCha20.

    Args:
        constants (dict): Dictionary containing "plaintext": bytes, "ciphertext": bytes , "nonce": bytes
        processes (int): Number of cpus to use. Reccomended is 1 less than your core count. Defaults to ((# of Logical Processors) / 2 - 1). 
    
    """

    if(processes == None):
        processes = int(cpu_count() / 2 - 1)

    with Pool(processes=processes, initializer=initialize_worker, initargs=(constants, )) as pool:
        results = pool.map(try_seed, range(2**32))
        seed = [s for s in results if s is not None]

        return seed

