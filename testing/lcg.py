# Group 7 - Austin Doucette
# CPSC 418 - Explorations of Pseudo Random Number Generation
# April 2025

class LCG:
    def __init__(self, multiplier=1103515245, increment=12345, modulus=31):
        self.state = 1
        self.multiplier = multiplier
        self.increment = increment
        self.modulus = 2**modulus - 1

    def seed(self, seed):
        self.state = seed % self.modulus

    def gen(self):
        self.state = (self.multiplier * self.state + self.increment) % self.modulus
        return self.state

    def generate_bits(self, bitcount):
        bits = ""

        while len(bits) < bitcount:
            num = self.gen()
            bits += bin(num)[2:] # Remove '0b'

        bits = bits[:bitcount]
        return bits
    
    def generate_bits_lsb(self, bitcount):
        bits = ""
        for _ in range(bitcount):
            num = self.gen()
            # print(f"Num: {num}, {bin(num % 2)}")
            bits += bin(num % 2)[2:]
            
        bits = bits[:bitcount]
        return bits
    
    def generate_bits_upper_32(self, bitcount):
        bits = ""
        while len(bits) < bitcount:
            num = (self.gen() >> 32) & 0xFFFFFFFF
            bits += bin(num)[2:] # Remove '0b'

        bits = bits[:bitcount]
        return bits
