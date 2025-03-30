#!/usr/bin/env python3
'''
p & q are large prime numebrs
n = pq
x_i = (x_i-1)^2 (mod n)
Seed = x0 s.t. gcd(x0, n)=1
Referenced: https://medium.com/@ntnprdhmm/how-to-generate-big-prime-numbers-miller-rabin-49e6e6af32fb
'''

import ctypes
import random
import math
import time
import os

"""BBS PRNG with 3 seed options: time, rand(), /dev/urandom"""
class BBS:
    def __init__(self, seed_type="time", bits=1024):
        #1034 bits for NIST testing
        self.p = self.generate_large_prime(bits)
        self.q = self.generate_large_prime(bits)
        self.n = self.p * self.q
        self.state = self.generate_seed(seed_type)
    """
    Generates a prime p ≡ 3 mod 4 (a Blum prime) needed for BBS.
    The ≡ 3 mod 4 condition ensures the required property of BBS is satisfied.
    """
    def generate_large_prime(self, bits):
        """Generate a large prime number with the specified number of bits."""
        while True:
            p = random.getrandbits(bits) # Get number of bit length
            # Ensure the number is odd and has the correct bit length
            # 1. Set MSB (bit_length-1 position) to ensure correct size
            # 2. Set LSB to 1 to ensure odd (primes > 2 must be odd)
            p |= (1 << bits - 1) | 1  

            # Adjust to satisfy p ≡ 3 mod 4 condition:
            # BBS requires this for its security proof to hold
            if p % 4 != 3:
                p += 2  # Next odd number (maintains oddness)

            if self.is_prime(p):
                return p

    """
    Probabilistic check if n is prime using Miller-Rabin
    parameters:
        n = number we are checking
        k = number of test rounds

    returns:
        True if n is prime
        False if n is composite
    """
    def is_prime(self, n, k=20):
        # Error check if n us less than or equal to 1, which cannot be a prime number
        if n <= 1:
            return False
        elif n <= 3:
            return True #Because we are taking the modulo of 4, numbers will be less than 3
        elif n % 2 == 0:
            return False # Even numbers greater than 2 are not prime

        # Find how many times 2 divides into d. Similar to finding the binary of exponent learnt in class
        # Fermat's Little Theorem: if n is prime, a^(n-1) = 1 (mod n)
        # n-1 = d*s^2
        d = n - 1
        s = 0 # Instantiate number of times 2 divides into d
        while d % 2 == 0:
            d //= 2 # Floor division
            s += 1

        #Testing k rounds
        for _ in range(k):
            # Choose a random witness integer for a between 2 and n-2 because 0, 1, or n-1 give false positives
            a = random.randint(2, n - 2)
            x = pow(a, d, n) # a^d (mod n)

            if x == 1 or x == n - 1: # Skip if modulo n is 1 or n-1 because these are trivial roots of unity 
                continue
            #Do repeated squaring to check 
            for __ in range(s - 1):
                x = pow(x, 2, n)
                if x == n - 1:
                    break   #Pass if -1 mod n (same as n-1 mod n) is found
            else:
                return False
        return True # If all tests are passed, then n is likely prime
    """
        Generates a seed based on the specified type.
        Options:
            - "time": Uses current time as seed
            - "rand": uses libc.rand() for random seed
            - "urandom": Reads from /dev/urandom
    """
    def generate_seed(self, seed_type):
        while True:
            if seed_type == "time":
                seed = int(time.time()*1_000_000) % self.n # Current time in microseconds
            elif seed_type == "rand":
                libc = ctypes.CDLL("libc.so.6")  # Load C library
                libc.srand(libc.time(0))  # Properly seed rand()
                seed = (libc.rand() << 32) | libc.rand()
                seed %= self.n
            elif seed_type == "urandom":
                seed = int.from_bytes(os.urandom(16), byteorder='big') % self.n
            else:
                raise ValueError("Invalid seed type. Choose 'time', 'rand', or 'urandom'.")
            if 1 < seed < self.n and math.gcd(seed, self.n) == 1: #Ensure seed is coprime with n
                return seed

    """
            Generates the next bit in the sequence using the BBS algorithm.
            The state is updated after each call.
    """
    def next_bit(self):
        self.state = pow(self.state, 2, self.n)
        return self.state % 2

    """
        Generate binary string for NIST testing
        Returns: '010101...' format (length = num_bits)
    """
    def generate_nist_output(self, num_bits=1_000_000):
        bits = []
        for _ in range(num_bits):
            bits.append(str(self.next_bit()))
        return ''.join(bits)

if __name__ == "__main__":
        #dev/urandom
        bbs = BBS("urandom", bits=1024) # 1024-bit primes for NIST
        nist_bits = bbs.generate_nist_output(1_000_000) # Generate 1 million bits (NIST minimum recommendation)
        # Save to file (NIST STS expects binary ASCII '0'/'1' format)
        with open("urand_bbs_nist_testdata.txt", "w") as f:
            f.write(nist_bits)
        print(f"Generated {len(nist_bits)} bits for NIST testing")
        print(f"First 100 bits: {nist_bits[:100]}...")
        print("Saved to 'urand_bbs_nist_testdata.txt'")

        #rand()
        bbs = BBS("rand", bits=1024) # 1024-bit primes for NIST
        nist_bits = bbs.generate_nist_output(1_000_000) # Generate 1 million bits (NIST minimum recommendation)
        # Save to file (NIST STS expects binary ASCII '0'/'1' format)
        with open("rand_bbs_nist_testdata.txt", "w") as f:
            f.write(nist_bits)
        print(f"Generated {len(nist_bits)} bits for NIST testing")
        print(f"First 100 bits: {nist_bits[:100]}...")
        print("Saved to 'rand_bbs_nist_testdata.txt'")

        #Time
        bbs = BBS("time", bits=1024) # 1024-bit primes for NIST
        nist_bits = bbs.generate_nist_output(1_000_000) # Generate 1 million bits (NIST minimum recommendation)
        # Save to file (NIST STS expects binary ASCII '0'/'1' format)
        with open("time_bbs_nist_testdata.txt", "w") as f:
            f.write(nist_bits)
        print(f"Generated {len(nist_bits)} bits for NIST testing")
        print(f"First 100 bits: {nist_bits[:100]}...")
        print("Saved to 'time_bbs_nist_testdata.txt'")