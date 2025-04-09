# Group 7 - Austin Doucette, Michelle Cheung
# CPSC 418 - Explorations of Pseudo Random Number Generation
# April 2025

from lcg import *
from bbs import *
from seed_gen import *

import os
import sys

""" 
    The goal of this file is to generate testing data for BBS and LCG using the same input seeds. See seed_gen.py for seed generation.

    Currently the LCG being used in the same one used by std.lib entitled rand(). 

    To run this file and generate pseudo random numbers for testing:
        1. Ensure that this file, lcg.py, bbs.py, and seed_gen.py are within the same directory. There should also be a directory named test_data at this level.

        2. Run this file with py generate_numbers.py with the following 4 command line arguments IN ORDER:
            - File count (int): The number of unique triplets to create. Each triplet contains the following pseudo random numbers:
                - BBS seeded with urand
                - BBS seeded with rand
                - BBS seeded with time
                - LCG seeded with urand
                - LCG seeded with rand
                - LCG seeded with time
            - Directory name (string): The name of the new directory in ./test_data where this data will be stored
            - Generate BBS (bool): A flag which determines if BBS data will be generated. Either True, or False
            - Generate LCG (bool): A flag which determines if LCG data will be generated. Either True, or False
                - If you generate LCG data and BBS data the shared seed must adhere to the seeding constraints (see seed_gen.py)
                - If you generate LCG without BBS data the seed used will not adhere to BBS seeding constraings (see seed_gen.py)

        3. If you are using an LCG you can then choose to either use the C rand function parameters or specify your own.
            - If you specify your own you can also choose to only use bits 32-63 instead of the whole output.

        3. The generated pseudo random numbers will be stored within the specified directory. 
            - Each file contains a single number of 1 million bits
            - The LCG and BBS file which use the same seed will have the same leading number and same seed postfix
"""



def get_data(file_count, path, gen_bbs, gen_lcg, lcg_params=None, upper_lcg=False):
    """
        Generates test data for both BBS and LCG and saves the data at the specified path.

        Args:
            file_count (int): Controls how many times BBS and LCG generate data for each 3 types of seeds.
            path (str): The name of the new directory contained within /test_data which stores this generated data. Example: "data_1".
            gen_bbs (bool): True: Generate BBS numbers, False: Do not generate BBS numbers.
            gen_lcg (bool): True: Generate LCG numbers, False: Do not generate LCG numbers.
            lcg_params (tuple): Contains (multiplier, increment, modulus) where modulus is the power of two not the literal number. Uses C rand by default.
    
    """

    MAIN_DIR = "./test_data"

    # Create the new directory
    try:
        os.makedirs(f"{MAIN_DIR + "/" + path}")
    except:
        print("Error creating directory!")
        return -1

    for iteration in range(file_count):
        fname_template = MAIN_DIR + "/" + path + "/" + str(iteration) + "_" # ./MAIN_DIR/path/iteration_

        bbs = BBS()
        m = bbs.get_m()

        # Generate valid seeds
        if(gen_bbs):
            s_urand = seed_bbs_urand(m)             # Use BBS seeds for both BBS and LCG
            s_rand = seed_bbs_rand(m)
            s_time = seed_bbs_time(m)
        else:
            s_urand = seed_standard_urand()        # Use less strict seeds (far faster!)
            s_rand = seed_standard_rand()
            s_time = seed_standard_time()

        ##################################
        #       BBS Data Generation
        ##################################
        if(gen_bbs):
            # urand
            bbs.seed(s_urand)
            data = bbs.generate_nist_output(1_000_000)
            fname = fname_template + "bbs_urand.txt"    # Final path = ./MAIN_DIR/path/iteration_bbs_urand.txt

            with open(f"{fname}", "w") as f:
                f.write(data)

            # rand
            bbs.seed(s_rand)
            data = bbs.generate_nist_output(1_000_000)
            fname = fname_template + "bbs_rand.txt"     # Final path = ./MAIN_DIR/path/iteration_bbs_rand.txt

            with open(f"{fname}", "w") as f:
                f.write(data)

            # time
            bbs.seed(s_time)
            data = bbs.generate_nist_output(1_000_000)
            fname = fname_template + "bbs_time.txt"     # Final path = ./MAIN_DIR/path/iteration_bbs_time.txt

            with open(f"{fname}", "w") as f:
                f.write(data)

        ##################################
        #       LCG Data Generation
        ##################################
        if(gen_lcg):
            if(lcg_params == None):
                lcg = LCG()
            else:
                lcg = LCG(lcg_params[0], lcg_params[1], lcg_params[2])
            
            # urand
            lcg.seed(s_urand)
            if(upper_lcg):
                data = lcg.generate_bits_upper_32(1_000_000)
            else:
                data = lcg.generate_bits(1_000_000)
            fname = fname_template + "lcg_urand.txt"    # Final path = ./MAIN_DIR/path/iteration_lcg_urand.txt

            with open(f"{fname}", "w") as f:
                f.write(data)

            # rand - very redundant, it is being seeded with itself...
            lcg.seed(s_rand)
            if(upper_lcg):
                data = lcg.generate_bits_upper_32(1_000_000)
            else:
                data = lcg.generate_bits(1_000_000)
            fname = fname_template + "lcg_rand.txt"    # Final path = ./MAIN_DIR/path/iteration_lcg_rand.txt 

            with open(f"{fname}", "w") as f:
                f.write(data)

            # time
            lcg.seed(s_time)
            if(upper_lcg):
                data = lcg.generate_bits_upper_32(1_000_000)
            else:
                data = lcg.generate_bits(1_000_000)
            fname = fname_template + "lcg_time.txt"    # Final path = ./MAIN_DIR/path/iteration_lcg_time.txt 

            with open(f"{fname}", "w") as f:
                f.write(data)



if __name__ == "__main__":
    try:
        gen_bbs = (sys.argv[3] == "true")
        gen_lcg = (sys.argv[4] == "true")

        if(gen_lcg):
            while True:
                try:
                    choice = input("Use C rand paramters for LCG (yes, no)? ")
                    if choice == "yes":
                        lcg_params = None
                        break
                    if choice == "no":
                        multipler = int(input("Provide multipler. "))
                        increment = int(input("Provide increment. "))
                        modulus = int(input("Provide modulus (as a power of 2, i.e. 2^input = modulus). "))
                        lcg_params = (multipler, increment, modulus)
                        upper_32 = (input("Use upper 32 bits only (yes, no)? ") == "yes")
                        break
                except:
                    print("Error, provide valid inputs.")
                    continue

        get_data(int(sys.argv[1]), sys.argv[2], gen_bbs, gen_lcg, lcg_params, upper_32)
    except Exception as e:
        print("Error! Call script with 4 arguments: file_count, dir_name, gen_bbs, gen_lcg.")
        print("\tfile_count (int): Number of unique triplets of data files to create.")
        print("\tdir_name (string): The name of the NEW directory in ./test_data where this data will be stored.")
        print("\tgen_bbs (bool): If BBS test data will be generated. Either false, or true.")
        print("\tgen_lcg (bool): If LCG test data will be generated. Either false, or true.")
        print(f"\n {e}")

