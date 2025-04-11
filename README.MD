# Explorations of Pseudo Random Number Generation

## CPSC 418 - Group 7 Final Project

Contains a simulated attack on symmetric key generation using bad PRNG and statistical testing of the Linear Congruential Generator, and the Blum-Blum Shub Geneartor using [stevenang - randomness_testsuite](https://github.com/stevenang/randomness_testsuite/tree/6a74f91dcac173052d81b26c45ee0d4e4a417d93). 


## Table of Contents
- [Installation](#installation)
- [Usage](#usage)
    - [Attack Demonstration](#attack-demonstration)
    - [Testing](#testing)


## Installation
#### Download
- Run: git clone --recurse-submodules https://github.com/plambi/CPSC418-Project

#### Libraries Required:
- PyCryptodome
- Numpy
- Scripy

## Usage

#### Attack Demonstration
The entry point to the simulation is within [showcase.py](attack_demonstration/showcase.py). For control over the simulation adjust the following parameters:
- lcg_range | This parameter controls the range of the initial seeding for the victims LCG which can be lowered below 31 (2^31 possible seeds) to demonstrate functionality in a reasonable amount of time.
- thread_count | Controls how many threads will be used.

#### Testing
###### Seed Generation [seed_gen.py](testing/seed_gen.py): 
- This file handles generating the seeds used for both BBS and LCG.
- Users do not need to directly call this.
###### Number Generation [generate_numbers.py](testing/generate_numbers.py): 
- Generates files containing 1 million bits of LCG/BBS pseudo random numbers. 
- py generate_numbers.py <file_count> <directory_name> <gen_bbs> <gen_lcg>
    - file_count: The number of triplets containing PRNG for lcg/bbs. Each triplet contains one file (for each algorithm) using each of the 3 seed types generated in [seed_gen.py](testing/seed_gen.py).
    - directory_name: Numbers are written to a new directory created within .\testing\test_data with this name.
    - gen_bbs: Boolean representing if BBS numbers will be generated, true or false.
    - gen_lcg: Boolean representing if LCG numbers will be generated, true or false.
###### Performing Tests [run_tests.py](testing/run_tests.py)
- Performs all tests from [randomness_testsuite](testing/randomness_testsuite/) on every test number within the directory and stores the results into a sub directory named results.
- py run_tests.py <input_dir>
###### Analyzing Test Data [analyze.py](testing/analyze.py)
- Analyzes test data and writes results into a sub directory called analyzed_results.
- py run_tests.py  <result_data_dir>
###### Full Example Run:
1. Navigate to the testing directory. The current path should be \CPSC418-Project\testing
2. Generate one triplet with both LCG and BBS for testing
    - py generate_numbers.py 1 my_test_data true true
        - Use C rand parameters for LCG (yes, no)?
            - yes: Uses LCG parameters a = 1103515245, c = 12345, m = 2^31 - 1
            - no: Prompts for parameter specification
        - Use only LSB for LCG (yes, no)?
            - yes: Each bit of the LCG number is produced using just the least significant bit of every generation
            - no: LCG generations are concatenated together to produce the final bit sequence
3. Perform the testing
    - py run_tests.py .\test_data\my_test_data
    - This can take quite a long time
4. Analyze the data
    - py analyze.py .\test_data\my_test_data\results
        - Is this only one generators data (yes, no)?
            - yes: If your data contains only LCG or BBS data
            - no: If your data contains both LCG and BBS data
5. The final analyzed data will be stored at .\test_data\my_test_data\results\overall_results.
