# Austin Doucette
# CPSC 418 - Project
# March 2025

import multiprocessing
import multiprocessing.process
from Crypto.Cipher import ChaCha20


kill_event = multiprocessing.Event()



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
    state = ((1103515245 * seed) + 12345) % 2147483648      # Call of rand
    keys.append(state.to_bytes(4, "big"))

    for _ in range(1, 8):
        state = ((1103515245 * state) + 12345) % 2147483648
        keys.append(state.to_bytes(4, "big"))

    result = b''
    for i in range(8):
        result += keys[i]

    return result



def try_seed(seed, constants):
    """ 
    Worker function. Generates a 256 bit key using seed and attempts decryption with it.
    
    Args:
        seed (int): LCG initial seeding value
        constants (dict): Dictionary containing "plaintext": bytes, "ciphertext": bytes , "nonce": bytes

    """
    key = generate_decryption_key(seed)
    cipher = ChaCha20.new(key=key, nonce=constants["nonce"])
    decrypted_ciphertext = cipher.decrypt(constants["ciphertext"])

    if(decrypted_ciphertext == constants["plaintext"]):
        return True
    return False



def worker(start, stop, constants, results):
    '''
    Checks all numbers from start to stop as seeds for the LCG based key.

    Args:
        start (int): The first candidate key
        stop (int): The last candidate key (exclusive)
        constants (dict): Dictionary containing "plaintext": bytes, "ciphertext": bytes , "nonce": bytes
        results (list): Multiprocessing manager list where results are stored
    
    '''
    for i in range(start, stop):
        # Stop thread if result has been found
        if(kill_event.is_set()):
            break
        
        # Try each seed
        if(try_seed(i, constants) == True):
            # If the true seed is found, signal other threads and store seed
            kill_event.set
            results.append(i)

    results.append(-1)



def brute_force(constants, thread_count: int, max_key_length: int):
    """
    Brute forces 32 bit LCG generated key encrypted with ChaCha20.

    Args:
        constants (dict): Dictionary containing "plaintext": bytes, "ciphertext": bytes , "nonce": bytes
        processes (int): Number of threads to create. Use CPU core count. 4 should be safe for everybody
        max_key_length (int): The power of two representing the number of keys that will be checked. Keys = 2^max_key_length
    
    """

    stop = 2**max_key_length - 1
    step = int(stop / thread_count + 1)

    thread_start = 0
    thread_stop = step

    with multiprocessing.Manager() as manager:
        results = manager.list()    # List for threads to store their results (-1 or some seed value)
        processes = []

        # Start the threads
        for i in range(thread_count + 1):
            p = multiprocessing.Process(target=worker, args=(thread_start, thread_stop, constants, results, ))
            processes.append(p)
            p.start()
            thread_start = thread_start + step  # Each thread operates on a range within the key space
            thread_stop = thread_stop + step

        for i in processes:
            i.join()
    
        r = list(results)

    # Return the found seed
    for i in r:
        if i != -1:
            return i
    return -1