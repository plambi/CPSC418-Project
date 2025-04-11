# Group 7 - Austin Doucette
# CPSC 418 - Explorations of Pseudo Random Number Generation
# April 2025


import os
import sys

"""
    The goal of this file is to compare the test results of LCG and BBS. 
    Data for all methods here are gotten by calling parse_directory_both() with the directory containing the test data. 
    There are methods that handle data generated using only one generator named xxx_xxx_single() instead of xxx_xxx_both() which were used for debugging.

    To run this file and analyze the results:
        1. Ensure that your test resulted are stored properly
            - They must be in a directory called test_data which is at the same level as this file
            - Assuming the data is generated using test.py and has not been moved it will work

        2. Run this file with one argument: 
            - Input data directory: The directory containing the data to be analyzed Example: ./test_data/test_a/results

        3. Choose which seeds you would like to analyze. 

        4. Choose if you are only analyzing one generators data
            - If so specify wether it is BBS or LCG

        5. The results from the analysis will be written to a new directory named "parsed_results" within your data directory
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



def parse_directory_single(directory, postfixes, generator):
    """
    Given a directory containing either LCG or BBS test results (not both!), parse into dictionaries for easy comparison.

    Args:
        directory (string): Directory containing test results. Example "./test_data/a_test/results"
        postfixes (list): Contains the postfixes for files to parse. Example ["rand", "urand", "time"]
        generator (string): Either "lcg" or "bbs"

    Returns:
        list: Contains the results of each test file stored as a dict.
    
    """

    if not(generator == "lcg") and not(generator == "bbs"):
        print("Error! Bad parameters in parse_directory_single. Argument generator must be either lcg or bbs")

    # Count the number of files
    file_count = 0
    for file in os.listdir(directory):
        path = os.path.join(directory, file)

        if(os.path.isfile(path)):
            file_count += 1

    test_results = []

    files_of_each_type = int((file_count) / len(postfixes))      # The number of triplets of files that exist

    # Iterate over all files and capture data
    for i in range(files_of_each_type):
        for postfix in postfixes:
            if generator == "bbs":
                bbs_file = directory + "/" + str(i) + "_bbs_" + postfix + ".txt"
                with open(bbs_file, "r") as f:
                    test_results.append(parse_individual_test(f.read()))
            else:
                lcg_file = directory + "/" + str(i) + "_lcg_" + postfix + ".txt"
                with open(lcg_file, "r") as f:
                    test_results.append(parse_individual_test(f.read()))

    return test_results



def parse_directory_both(directory, postfixes, lcg_only=False):
    """
    Given a directory containing LCG and BBS test results, parse into dictionaries for easy comparison.

    Args:
        directory (string): Directory containing test results. Example "./test_data/a_test/results"
        postfixes (list): Contains the postfixes for files to parse. Example ["rand", "urand", "time"]
        lcg_only (bool): If true only the LCG files will be parsed and returned. 

    Returns:
        dict: Contains 2 values: lcg and bbs. Both are lists containing dictionaries representing the test results. Example {"lcg_test_results": [{"1. Frequency Test": (0.22, False), "2. Block Frequency Test": ...}, {"1. Frequency Test": ...}, ...], "bbs_test_results": ...}

    """

    # Count the number of files
    file_count = 0
    for file in os.listdir(directory):
        path = os.path.join(directory, file)

        if(os.path.isfile(path)):
            file_count += 1

    bbs_test_results = []
    lcg_test_results = []

    if not lcg_only:
        files_of_each_type = int((file_count) / 6)      # The number of triplets of files that exist
    else:
        files_of_each_type = int((file_count) / 3)

    # Iterate over all files and capture data
    for i in range(files_of_each_type):
        for postfix in postfixes:
            if not lcg_only:
                bbs_dir = directory + "/" + str(i) + "_bbs_" + postfix + ".txt"
                with open(bbs_dir, "r") as f:
                    bbs_test_results.append(parse_individual_test(f.read()))

            lcg_dir = directory + "/" + str(i) + "_lcg_" + postfix + ".txt"
            with open(lcg_dir, "r") as f:
                lcg_test_results.append(parse_individual_test(f.read()))

    if lcg_only:
        return lcg_test_results
    else:
        results = {"bbs": bbs_test_results, "lcg": lcg_test_results}
        return results



def total_passes_single(test_results):
    """
        Determines the total number of passes across all tests for only 1 PRNG.

        Args:
            test_results (list): List returned from parse_directory. Can be either BBS or LCG.

        Returns:
            tuple: (passes, total_tests)
    """

    # Get passes
    passes = 0

    for result in test_results:
        r = result["11. Serial Test"]   # Handle the Serial Test individually since it produces 2 results
        if r[0][1] == True:
            passes += 1
        if r[1][1] == True:
            passes += 1
        result.pop("11. Serial Test")

        for test in result:             # Count passes
            if result[test][1] == True:
                passes += 1
        
        result["11. Serial Test"] = r   # Add the serial test back

    individual_tests = 15
    total_tests = len(test_results) * individual_tests

    return (passes, total_tests)



def total_passes_both(lcg_test_results, bbs_test_results):
    """
        Determines the total number of passes across all tests.

        Args:
            lcg_test_results (list): List returned from parse_directory.
            bbs_test_results (list): List returned from parse_directory.

        Returns:
            tuple: (LCG_passes, BBS_passes, total_tests)
    """

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



def passes_single(test_results):
    """
        Determines how many times each test was passed. I.e. how many times did it pass Frequency, Block Frequency, etc...

        Args:
            test_results (list): List returned from parse_directory. Can be either LCG or BBS

        Returns:
            string: The results as a string.
    
    """

    # Create a template dictionary containing all tests
    passes = {}
    for test in test_results[0]:
        passes[test] = 0


    # For every pair of result files
    for i in range(len(test_results)):
        #  For every test
        for test in passes:
            if test == "11. Serial Test":
                result_1 = test_results[i][test][0][1]
                result_2 = test_results[i][test][1][1]

                if result_1:
                    passes[test] += 1
                if  result_2:
                    passes[test] += 1
            else:
                lcg_result = test_results[i][test][1]

                if lcg_result:
                    passes[test] += 1
    
    lines = []
    total_passes, total_tests = total_passes_single(test_results)
    lines.append(f"Overall\n")
    lines.append(f"\tPassed: {round((total_passes / total_tests) * 100, 2)}% of tests. {total_passes}/{total_tests}\n\n")

    for test in passes:
        if test == "11. Serial Test":
            total_tests = len(test_results) * 2
        else:
            total_tests = len(test_results)

        lines.append(f"{test}\n")
        lines.append(f"\tPassed: {round((passes[test] / total_tests) * 100, 2)}% of the time. {passes[test]}/{total_tests}\n\n")

    final_string = "".join(lines)
    return final_string



def passes_both(lcg_test_results, bbs_test_results):
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
    total_lcg, total_bbs, total = total_passes_both(lcg_test_results, bbs_test_results)
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



def calculate_results_single(directory, output_file_name, postfixes, generator):
    """
        Parses all available data in the directory and writes summary files within a sub directory named "parsed_results".

        Args:
            directory (string): The directory to the SP800-22 results generated by tests.py. Example "./test_data/test_a/results"
            output_file_name (string): The header for the output file name. Example output_file_name = result, filename = "result_passes.txt"
            postfixes (list): Only files with the specified postfixes will be parsed. Example: ["rand", "urand", "time"]
            generator (string): Either lcg or bbs. Needed for input file name determination.
    
    """
    results = parse_directory_single(directory, postfixes, generator)

    # Make the directory
    os.makedirs(f"{directory}/analyzed_results", exist_ok=True)

    # Compute and write the output data
    of = f"{directory}/analyzed_results/{output_file_name}_passes.txt"
    with open(of, "w") as f:
        f.write(passes_single(results))



def calculate_results_both(directory, output_file_name, postfixes):
    """
        Parses all available data in the directory and writes summary files within a sub directory named "parsed_results". Produces two files: passes.txt (independent pass rates), comparative_passes.txt (compares results with the same seed).

        Args:
            directory (string): The directory to the SP800-22 results generated by tests.py. Example "./test_data/test_a/results"
    
    """
    results = parse_directory_both(directory, postfixes)
    lcg = results["lcg"]
    bbs = results["bbs"]

    # Make the directory
    os.makedirs(f"{directory}/analyzed_results", exist_ok=True)

    # Compute and write the output data
    of = f"{directory}/analyzed_results/{output_file_name}_passes.txt"
    with open(of, "w") as f:
        f.write(passes_both(lcg, bbs))



if __name__ == "__main__":
    all_flag = False
    postfixes = ["rand", "urand", "time"]
    while True:
        try:
            both_flag = input("Is this only one generators data (yes, no)? ")
            if(both_flag == "yes"):
                which_generator = input("Which generator is it (lcg, bbs)? ")
                calculate_results_single(sys.argv[1], "rand", ["rand"], which_generator)
                calculate_results_single(sys.argv[1], "urand", ["urand"], which_generator)
                calculate_results_single(sys.argv[1], "time", ["time"], which_generator)
                calculate_results_single(sys.argv[1], "overall", postfixes, which_generator)
            else:
                if not(both_flag == "yes"):
                    calculate_results_both(sys.argv[1], "rand", ["rand"])
                    calculate_results_both(sys.argv[1], "urand", ["urand"])
                    calculate_results_both(sys.argv[1], "time", ["time"])
                    calculate_results_both(sys.argv[1], "overall", postfixes)
            break
        except Exception as e:
            print("Error! Call script with the data directory as the argument. Example: py analyze.py ./test_data/test_a/results")
            print(e)
