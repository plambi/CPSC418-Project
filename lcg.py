# Group 7 - Austin Doucette
# CPSC 418 - Explorations of Pseudo Random Number Generation
# April 2025

class LCG:
    def __init__(self,multiplier=1103515245, increment=123456, modulus=31):
        self.state = 0
        self.multiplier = multiplier
        self.increment = increment
        self.modulus = 2**modulus

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
