# Group 7 - Austin Doucette
# CPSC 418 - Explorations of Pseudo Random Number Generation
# April 2025


import os
import sys

"""
    The goal of this file is to compare the test results of LCG and BBS. Data for all methods here are gotten by calling parse_directory() with the directory containing the test data.

    To run this file and analyze the results:
        1. Ensure that your test resulted are stored properly
            - They must be in a directory called test_data which is at the same level as this file
            - Assuming the data is generated using test.py (with both BBS and LCG data) and has not been moved it will work

        2. Run this file with the your desired directory as the only argument. 
            - Example: py analyze.py ./test_data/test_a/results

        3. The results from the analysis will be written to a new directory named "parsed_results" within your data directory
"""

def parse_individual_test(test):
    """
        Parses a single test file result:

        Args:
            test (string): The string representation of the entirety of the test results.

        Results:
            dict: Keys = Test name, Values = results as a tuple. Example {"1. Frequency Test": (0.029257461551978524, True), ...}
    """

    result = {}

    lines = test.split("\n")
    for line in lines:
        if line == "":
            return result
        name, data = line.split(":")
        r = eval(data.strip())
        result[name] = r

    return result



def parse_directory(directory):
    """
    Given a directory containing LCG and BBS test results, parse into dictionaries for easy comparison.

    Args:
        directory (string): Directory containing test results. Example "./test_data/a_test/results"

    Returns:
        dict: Contains 2 values: lcg and bbs. Both are lists containing dictionaries representing the test results. Example {"lcg_test_results": [{"1. Frequency Test": (0.22, False), "2. Block Frequency Test": ...}, {"1. Frequency Test": ...}, ...], "bbs_test_results": ...}

    """
    POSTFIXES = ["rand", "urand", "time"]       # If the file naming format changes, these must be updated!!!

    # Count the number of files
    file_count = 0
    for file in os.listdir(directory):
        path = os.path.join(directory, file)

        if(os.path.isfile(path)):
            file_count += 1

    bbs_test_results = []
    lcg_test_results = []

    files_of_each_type = int((file_count) / 6)      # The number of triplets of files that exist

    # Iterate over all files and capture data
    for i in range(files_of_each_type):
        for postfix in POSTFIXES:
            with open(f"{directory + "/" + str(i) + "_bbs_" + postfix + ".txt"}", "r") as f:
                bbs_test_results.append(parse_individual_test(f.read()))
            with open(f"{directory + "/" + str(i) + "_lcg_" + postfix + ".txt"}", "r") as f:
                lcg_test_results.append(parse_individual_test(f.read()))

    results = {"bbs": bbs_test_results, "lcg": lcg_test_results}
    return results



def total_passes(lcg_test_results, bbs_test_results):
    """
        Determines the total number of passes across all tests.

        Args:
            lcg_test_results (list): List returned from parse_directory.
            bbs_test_results (list): List returned from parse_directory.

        Returns:
            tuple: (LCG_passes, BBS_passes)
    """

    # Get number of passes and fails
    bbs_passes = 0

    for result in bbs_test_results:
        r = result["11. Serial Test"]   # Handle the Serial Test individually since it produces 2 results
        if r[0][1] == True:
            bbs_passes += 1
        if r[1][1] == True:
            bbs_passes += 1
        result.pop("11. Serial Test")

        for test in result:             # Count passes
            if result[test][1] == True:
                bbs_passes += 1
        
        result["11. Serial Test"] = r   # Add the serial test back

    lcg_passes = 0

    for result in lcg_test_results:
        r = result["11. Serial Test"]   # Handle the Serial Test individually since it produces 2 results
        if r[0][1] == True:
            lcg_passes += 1
        if r[1][1] == True:
            lcg_passes += 1
        result.pop("11. Serial Test")

        for test in result:             # Count passes
            if result[test][1] == True:
                lcg_passes += 1
        
        result["11. Serial Test"] = r   # Add the serial test back

    individual_tests = 15
    total_tests = len(lcg_test_results) * individual_tests

    return (lcg_passes, bbs_passes, total_tests)



def passes(lcg_test_results, bbs_test_results):
    """
        Determines how many times each test was passed. I.e. how many times did LCG pass Frequency, Block Frequency, etc...

        Args:
            lcg_test_results (list): List returned from parse_directory.
            bbs_test_results (list): List returned from parse_directory.

        Returns:
            string: The results as a string.
    
    """

    # Create a template dictionary containing all tests
    template_dict = {}
    for test in lcg_test_results[0]:
        template_dict[test] = 0

    lcg_passes = template_dict.copy()
    bbs_passes = template_dict.copy()

    # For every pair of result files
    for i in range(len(lcg_test_results)):
        #  For every test
        for test in template_dict:
            if test == "11. Serial Test":
                bbs_result_1 = bbs_test_results[i][test][0][1]
                bbs_result_2 = bbs_test_results[i][test][1][1]
                lcg_result_1 = lcg_test_results[i][test][0][1]
                lcg_result_2 = lcg_test_results[i][test][1][1]

                if bbs_result_1:
                    bbs_passes[test] += 1
                if  bbs_result_2:
                    bbs_passes[test] += 1
                if lcg_result_1:
                    lcg_passes[test] += 1
                if  lcg_result_2:
                    lcg_passes[test] += 1
            else:
                bbs_result = bbs_test_results[i][test][1]
                lcg_result = lcg_test_results[i][test][1]

                if bbs_result:
                    bbs_passes[test] += 1
                if lcg_result:
                    lcg_passes[test] += 1
    
    lines = []
    total_lcg, total_bbs, total = total_passes(lcg_test_results, bbs_test_results)
    lines.append(f"Overall\n")
    lines.append(f"\tBBS passed: {round((total_bbs / total) * 100, 2)}% of tests. {total_bbs}/{total}\n")
    lines.append(f"\tLCG passed: {round((total_lcg / total) * 100, 2)}% of tests. {total_lcg}/{total}\n\n")

    for test in template_dict:
        if test == "11. Serial Test":
            total_tests = len(lcg_test_results) * 2
        else:
            total_tests = len(lcg_test_results)

        lines.append(f"{test}\n")
        lines.append(f"\tBBS passed: {round((bbs_passes[test] / total_tests) * 100, 2)}% of the time. {bbs_passes[test]}/{total_tests}\n")
        lines.append(f"\tLCG passed: {round((lcg_passes[test] / total_tests) * 100, 2)}% of the time. {lcg_passes[test]}/{total_tests}\n\n")

    final_string = "".join(lines)
    return final_string
            


def comparitive_passes(lcg_test_results, bbs_test_results):
    """ 
        Determines how often LCG and BBS agree on a result. I.e. do they both pass the same test. Both lists are alligned such that each entry in lcg uses the same seed as that entry in bbs.

        Args:
            lcg_test_results (list): List returned from parse_directory.
            bbs_test_results (list): List returned from parse_directory.

        Returns:
            string: The results as a string.
    
    """

    # Create a template dictionary containing all tests
    template_dict = {}
    for test in lcg_test_results[0]:
        template_dict[test] = 0

    # Create data dictionaries
    bbs_pass_lcg_pass = template_dict.copy()
    bbs_pass_lcg_fail = template_dict.copy()
    lcg_pass_bbs_pass = template_dict.copy()
    lcg_pass_bbs_fail = template_dict.copy()
    bbs_pass = template_dict.copy()
    lcg_pass = template_dict.copy()

    # For each pair of results
    for i in range(len(lcg_test_results)):
        # For each test
        for test in template_dict:
            # Manually do the serial test due to it having two values
            if test == "11. Serial Test":       
                bbs_result = bbs_test_results[i][test][0][1]    # Let the rest of the code handle one value
                lcg_result = lcg_test_results[i][test][0][1]
                bbs_result_2 = bbs_test_results[i][test][1][1]  # Handle the other value manually
                lcg_result_2 = lcg_test_results[i][test][1][1]

                # Both passed
                if bbs_result_2 and lcg_result_2:
                    bbs_pass_lcg_pass[test] += 1
                    lcg_pass_bbs_pass[test] += 1
                    bbs_pass[test] += 1
                    lcg_pass[test] += 1
                    
                # BBS passed, LCG failed
                elif bbs_result_2 and not lcg_result_2:
                    bbs_pass_lcg_fail[test] += 1
                    bbs_pass[test] += 1

                # LCG passed, BBS failed
                elif not bbs_result_2 and lcg_result_2:
                    lcg_pass_bbs_fail[test] += 1
                    lcg_pass[test] += 1

            # Handle other tests normally
            else:
                bbs_result = bbs_test_results[i][test][1]
                lcg_result = lcg_test_results[i][test][1]
                
            # Both passed
            if bbs_result and lcg_result:
                bbs_pass_lcg_pass[test] += 1
                lcg_pass_bbs_pass[test] += 1
                bbs_pass[test] += 1
                lcg_pass[test] += 1
                
            # BBS passed, LCG failed
            elif bbs_result and not lcg_result:
                bbs_pass_lcg_fail[test] += 1
                bbs_pass[test] += 1

            # LCG passed, BBS failed
            elif not bbs_result and lcg_result:
                lcg_pass_bbs_fail[test] += 1
                lcg_pass[test] += 1

    lines = []
    for test in template_dict:
        if test == "11. Serial Test":
            total_tests = len(lcg_test_results) * 2
        else:
            total_tests = len(lcg_test_results)

        lines.append(f"{test}\n")
        lines.append(f"\tBBS passed: {round((bbs_pass[test] / total_tests) * 100, 2)}% of the time\n")
        lines.append(f"\tLCG passed: {round((lcg_pass[test] / total_tests) * 100, 2)}% of the time\n")
        lines.append(f"\tGiven BBS passed, LCG passed {round((bbs_pass_lcg_pass[test] / total_tests) * 100, 2)}% of the time\n")
        lines.append(f"\tGiven BBS passed, LCG failed {round((bbs_pass_lcg_fail[test] / total_tests) * 100, 2)}% of the time\n")
        lines.append(f"\tGiven LCG passed, BBS passed {round((lcg_pass_bbs_pass[test] / total_tests) * 100, 2)}% of the time\n")
        lines.append(f"\tGiven LCG passed, BBS failed {round((lcg_pass_bbs_fail[test] / total_tests) * 100, 2)}% of the time\n\n")

    final_string = "".join(lines)

    return final_string



def calculate_results(directory):
    """
        Parses all available data in the directory and writes summary files within a sub directory named "parsed_results". Produces two files: passes.txt (independent pass rates), comparative_passes.txt (compares results with the same seed).

        Args:
            directory (string): The directory to the SP800-22 results generated by tests.py. Example "./test_data/test_a/results"
    
    """
    results = parse_directory(directory)
    lcg = results["lcg"]
    bbs = results["bbs"]

    # Make the directory
    os.makedirs(f"{directory}/parsed_results", exist_ok=True)

    # Compute and write the output data
    with open(f"{directory}/parsed_results/passes.txt", "w") as f:
        f.write(passes(lcg, bbs))
    with open(f"{directory}/parsed_results/comparative_passes.txt", "w") as f:
        f.write(comparitive_passes(lcg, bbs))

if __name__ == "__main__":
    try:
        calculate_results(sys.argv[1])
    except Exception as e:
        print("Error! Call script with the data directory as an argument. Example: ./test_data/test_a/results")
