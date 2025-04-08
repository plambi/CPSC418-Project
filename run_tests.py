# Group 7 - Austin Doucette, Michelle Cheung, Dayee Lee
# CPSC 418 - Explorations of Pseudo Random Number Generation
# April 2025

import os
import sys
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

# List of your files
files = [
    "./bbs/rand_bbs_nist_testdata.txt",
    "./bbs/time_bbs_nist_testdata.txt",
    "./bbs/urand_bbs_nist_testdata.txt"
]

def run_tests_and_save():
    """Run all tests and save consolidated results"""
    output_file = f"BBS_test_results.log"
    
    with open(output_file, 'w') as out_f:
        out_f.write(f"BBS PRNG Test Results\n")
        out_f.write("="*80 + "\n\n")
        
        for file in files:
            try:
                with open(file, 'r') as f:
                    bitstring = f.read().strip()
                
                print(f"\n=== Testing {file} ===")
                out_f.write(f"=== {os.path.basename(file)} ===\n")
                
                test_data = bitstring[:1000000]  # Use first 1M bits
                
                # Run and save all tests
                out_f.write(f"1. Frequency Test: {FrequencyTest.monobit_test(test_data)}\n")
                out_f.write(f"2. Block Frequency Test: {FrequencyTest.block_frequency(test_data)}\n")
                out_f.write(f"3. Runs Test: {RunTest.run_test(test_data)}\n")
                out_f.write(f"4. Longest Run of Ones: {RunTest.longest_one_block_test(test_data)}\n")
                out_f.write(f"5. Binary Matrix Rank: {Matrix.binary_matrix_rank_text(test_data)}\n")
                out_f.write(f"6. Spectral Test: {SpectralTest.spectral_test(test_data)}\n")
                out_f.write(f"7. Non-overlapping Template: {TemplateMatching.non_overlapping_test(test_data, '000000001')}\n")
                out_f.write(f"8. Overlapping Template: {TemplateMatching.overlapping_patterns(test_data)}\n")
                out_f.write(f"9. Universal Test: {Universal.statistical_test(test_data)}\n")
                out_f.write(f"10. Linear Complexity: {ComplexityTest.linear_complexity_test(test_data)}\n")
                out_f.write(f"11. Serial Test: {Serial.serial_test(test_data)}\n")
                out_f.write(f"12. Approximate Entropy: {ApproximateEntropy.approximate_entropy_test(test_data)}\n")
                out_f.write(f"13. Cumulative Sums (Forward): {CumulativeSums.cumulative_sums_test(test_data, 0)}\n")
                out_f.write(f"14. Cumulative Sums (Reverse): {CumulativeSums.cumulative_sums_test(test_data, 1)}\n")
                
                # Random Excursions
                out_f.write("\n15. Random Excursions:\n")
                for item in RandomExcursions.random_excursions_test(test_data):
                    out_f.write(f"\tState {item[0]}: P-value = {item[3]}, {'Pass' if item[4] >= 0.01 else 'Fail'}\n")
                
                out_f.write("\n16. Random Excursions Variant:\n")
                for item in RandomExcursions.variant_test(test_data):
                    out_f.write(f"\tState {item[0]}: P-value = {item[3]}, {'Pass' if item[4] >= 0.01 else 'Fail'}\n")
                
                out_f.write("\n" + "="*80 + "\n\n")
                print(f"Results for {file} saved to {output_file}")
                
            except FileNotFoundError:
                print(f"Error: {file} not found")
            except Exception as e:
                print(f"Error testing {file}: {str(e)}")
    
    print(f"\nAll results saved to {output_file}")

if __name__ == "__main__":
    run_tests_and_save()
