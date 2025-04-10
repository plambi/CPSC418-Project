# Group 7 - Austin Doucette, Michelle Cheung
# CPSC 418 - Explorations of Pseudo Random Number Generation
# April 2025

import os
import math
import time 

from lcg import *

"""
    The goal of this file is to generate seeds which can be used by both LCG and BBS for consistent testing.

    The first 3 methods (seed_bbs_urand, seed_bbs_rand, seed_bbs_time) all require you to pass in the m value (p * q) for your desired BBS class.
    The last 3 methods (standard_bbs_urand, standard_bbs_rand, standard_bbs_time) do not consider m. Currently they are unused.

"""

def seed_bbs_urand(m):
    """ 
    Generate a seed using urand that is coprime with n. 
    
    Args:
        m (int): p * q of bbs.
    """

    while True:
        seed = int.from_bytes(os.urandom(16), byteorder='big')

        # Valid seeds must be coprime with m
        if math.gcd(seed, m) == 1:
            return seed
        

def seed_bbs_rand(m):
    """ 
        Generate a seed using the C standard rand function.

        Args:
            m (int): p * q of bbs.
    
    """
    lcg = LCG()                                 # Default parameters are that of the C rand function
    lcg.seed(int(time.time() * 1000000))        # Current time in microseconds

    while True:
        seed = lcg.gen()

        # Valid seeds must be coprime with m
        if math.gcd(seed, m) == 1:
            return seed
        
def seed_bbs_time(m):
    """ 
        Generate a seed using time alone.

        Args:
            m (int): p * q of bbs.
    
    """
    while True:
        seed = int(time.time() * 1000000)

        # Valid seeds must be coprime with m
        if math.gcd(seed, m) == 1:
            return seed
    
def seed_standard_urand():
    """ Returns a 16 byte integer generated using urand. """
    seed = int.from_bytes(os.urandom(16), byteorder='big')
    return seed

def seed_standard_rand():
    """ Returns the result of rand() with a seed derived from the current time. """
    lcg = LCG()                             # Default parameters are that of the C rand function
    lcg.seed(int(time.time() * 1000000))   # Current time in microseconds
    return lcg.gen()

def seed_standard_time():
    """ Returns an integer representing the current time. """
    seed = int(time.time() * 1000000)       # Current time in microseconds
    return seed