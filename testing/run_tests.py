# Group 7 - Austin Doucette, Michelle Cheung
# CPSC 418 - Explorations of Pseudo Random Number Generation
# April 2025

"""
    This script performs the SP800-22 testing suite implemented by stevenang at https://github.com/stevenang/randomness_testsuite

    To run these tests do the following:

        1. Generate pseudo random numbers and store them as a string of bits on one line. Store as many of these as you would like in one directory.
            - To use our generation see generate_numbers.py
        
        2. Run this script and pass the directory containing the test files as an argument. 
            - Example: py run_tests.py ./test_data/my_data

        3. The results of each test will be saved to a new directory within the passed directory named results. The result of an input file shares a name with the input file.
"""

import sys
import os

testsuite_path = os.path.abspath("./randomness_testsuite")
sys.path.insert(0, testsuite_path)

from randomness_testsuite.FrequencyTest import FrequencyTest
from randomness_testsuite.RunTest import RunTest
from randomness_testsuite.Matrix import Matrix
from randomness_testsuite.Spectral import SpectralTest
from randomness_testsuite.TemplateMatching import TemplateMatching
from randomness_testsuite.Universal import Universal
from randomness_testsuite.Complexity import ComplexityTest
from randomness_testsuite.Serial import Serial
from randomness_testsuite.ApproximateEntropy import ApproximateEntropy
from randomness_testsuite.CumulativeSum import CumulativeSums
from randomness_testsuite.RandomExcursions import RandomExcursions

import numpy

numpy.set_printoptions(precision=16, suppress=False) # Allows proper printing on windows

def run_on_dir(directory):
    """
        Runs the NIST SP800-22 testing suite written by https://github.com/stevenang/randomness_testsuite

        Args:
            directory (string): The directory to test.
    
    """

    # Gather all input file paths
    files = []
    for file in os.listdir(directory):
        path = os.path.join(directory, file)

        if(os.path.isfile(path)):
            files.append(path)

    # Create the results directory
    results_path = directory + "/" + "results"
    try:
        os.makedirs(results_path, exist_ok=True)
    except:
        print("Error creating directory!")
        return -1
    
    for file in files:
        # Read bits
        with open(file, "r") as f:
            bits = f.read().strip()

        test_data = bits[:1000000]      # Isolate first million bits (fairly certain this is redundant)

        # Run and save all tests
        results = []
        r = FrequencyTest.monobit_test(test_data)                   # This parsing is because for some reason values are printed as (np.float(), np.bool())
        parsed_r = (float(r[0]), bool(r[1]))
        results.append(f"1. Frequency Test: {parsed_r}\n")

        r = FrequencyTest.block_frequency(test_data)
        parsed_r = (float(r[0]), bool(r[1]))
        results.append(f"2. Block Frequency Test: {parsed_r}\n")

        r = RunTest.run_test(test_data)
        parsed_r = (float(r[0]), bool(r[1]))
        results.append(f"3. Runs Test: {parsed_r}\n")

        r = RunTest.longest_one_block_test(test_data)
        parsed_r = (float(r[0]), bool(r[1]))
        results.append(f"4. Longest Run of Ones: {parsed_r}\n")

        r = Matrix.binary_matrix_rank_text(test_data)
        parsed_r = (float(r[0]), bool(r[1]))
        results.append(f"5. Binary Matrix Rank: {parsed_r}\n")
        
        r = SpectralTest.spectral_test(test_data)
        parsed_r = (float(r[0]), bool(r[1]))
        results.append(f"6. Spectral Test: {parsed_r}\n")

        r = TemplateMatching.non_overlapping_test(test_data, verbose=False, template_pattern='000000001')
        parsed_r = (float(r[0]), bool(r[1]))
        results.append(f"7. Non-overlapping Template: {parsed_r}\n")

        r = TemplateMatching.overlapping_patterns(test_data)
        parsed_r = (float(r[0]), bool(r[1]))
        results.append(f"8. Overlapping Template: {parsed_r}\n")

        r = Universal.statistical_test(test_data)
        parsed_r = (float(r[0]), bool(r[1]))
        results.append(f"9. Universal Test: {parsed_r}\n")

        r = ComplexityTest.linear_complexity_test(test_data)
        parsed_r = (float(r[0]), bool(r[1]))
        results.append(f"10. Linear Complexity: {parsed_r}\n")

        r = Serial.serial_test(test_data)
        parsed_r = ((float(r[0][0]), bool(r[0][1])), (float(r[1][0]), bool(r[1][1])))   # Special: Returns ((pval, pass), (pval, pass))
        results.append(f"11. Serial Test: {parsed_r}\n")

        r = ApproximateEntropy.approximate_entropy_test(test_data)
        parsed_r = (float(r[0]), bool(r[1]))
        results.append(f"12. Approximate Entropy: {parsed_r}\n")

        r = CumulativeSums.cumulative_sums_test(test_data, 0)
        parsed_r = (float(r[0]), bool(r[1]))
        results.append(f"13. Cumulative Sums (Forward): {parsed_r}\n")

        r = CumulativeSums.cumulative_sums_test(test_data, 1)
        parsed_r = (float(r[0]), bool(r[1]))
        results.append(f"14. Cumulative Sums (Reverse): {parsed_r}\n")

        # Random Excursions
        results.append("\n15. Random Excursions:\n")
        for item in RandomExcursions.random_excursions_test(test_data):
            results.append(f"\tState {item[0]}: P-value = {item[3]}, {'Pass' if item[4] >= 0.01 else 'Fail'}\n")
        
        results.append("\n16. Random Excursions Variant:\n")
        for item in RandomExcursions.variant_test(test_data):
            results.append(f"\tState {item[0]}: P-value = {item[3]}, {'Pass' if item[4] >= 0.01 else 'Fail'}\n")

        # Write results to output file
        fname = os.path.basename(file)
        fpath = results_path + "/" + fname
        with open(fpath, "w") as rfile:
            for line in results:
                rfile.write(line)
        
        print(f"Results of {fname} saved to {fpath}.")


if __name__ == "__main__":
    try:
        run_on_dir(sys.argv[1])
    except:
        print("Error! Call script with 1 argument: path")
        print("\t path (string): The directory path of the directory to test. Example: ./test_data/my_data")