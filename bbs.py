# Group 7 - Austin Doucette, Michelle Cheung, Dayee Lee
# CPSC 418 - Project
# April 2025

'''
p & q are large prime numebrs
n = pq
x_i = (x_i-1)^2 (mod n)
Seed = x0 s.t. gcd(x0, n)=1
Referenced: https://medium.com/@ntnprdhmm/how-to-generate-big-prime-numbers-miller-rabin-49e6e6af32fb
'''

import random

class BBS:
    def __init__(self, bits=1024):
        #1024 bits for NIST testing
        self.p = self.generate_large_prime(bits)
        self.q = self.generate_large_prime(bits)
        self.m = self.p * self.q

    def get_m(self):
        return self.m

    def seed(self, seed):
        self.state = seed

    def generate_large_prime(self, bits):
        """ Generates a large prime p ≡ 3 mod 4 (a Blum prime) needed for BBS with the specified number of bits. """
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

    def is_prime(self, n, k=20):
        """
        Probabilistic check if n is prime using Miller-Rabin.

        Args:
            n = number we are checking
            k = number of test rounds

        Returns:
            True: if n is prime
            False: if n is composite
        """
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

    def next_bit(self):
        """ Generates the next bit in the sequence using the BBS algorithm. The state is updated after each call. """
        self.state = pow(self.state, 2, self.m)
        return self.state % 2

    def generate_nist_output(self, num_bits=1_000_000):
        """
        Generate binary string for NIST testing.

        Returns: '010101...' format (length = num_bits)
        """
        bits = []
        for _ in range(num_bits):
            bits.append(str(self.next_bit()))
        return ''.join(bits)
