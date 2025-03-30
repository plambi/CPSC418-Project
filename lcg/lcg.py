import time
import os

class LCG:
    def __init__(self,multiplier=1103515245, increment=123456, modulus=31):
        self.seed = 0
        self.multiplier = multiplier
        self.increment = increment
        self.modulus = 2**modulus

    def generate_seed(self, seed_type):
        if seed_type == "time":
            self.seed = int(time.time() * 1000) % self.modulus
        elif seed_type == "urandom":
            self.seed = int.from_bytes(os.urandom(self.modulus), byteorder='big') % self.modulus
        else:
            self.seed = 0

    def gen(self):
        self.seed = (self.multiplier * self.seed + self.increment) % self.modulus
        return self.seed

    def generate_bits(self, bitcount):
        bits = ""
        while len(bits) < bitcount:
            num = self.gen()
            bits += bin(num)[2:] # Remove '0b'

        bits = bits[:bitcount]
        return bits

if __name__ == "__main__":
    lcg = LCG()
    lcg.generate_seed("time")
    bits = lcg.generate_bits(1_000_000)
    # Save the bits to a file
    with open("time_lcg_nist_testdata.txt", "w") as f:
        f.write(bits)

    lcg.generate_seed("urandom")
    bits = lcg.generate_bits(1_000_000)
    # Save the bits to a file
    with open("urand_lcg_nist_testdata.txt", "w") as f:
        f.write(bits)

    lcg.generate_seed("none")
    bits = lcg.generate_bits(1_000_000)
    # Save the bits to a file
    with open("zero_lcg_nist_testdata.txt", "w") as f:
        f.write(bits)
