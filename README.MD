randomness_testsuite: https://github.com/stevenang/randomness_testsuite 

Data Generation:
    To generate test data run generate_numbers.py with 2 command line arguments: 
        - file_count (int): Number of unique triplets of data files to create.
        - dir_name (string): The name of the NEW directory in ./test_data where this data will be stored (must be unique).

    This will produce files with 1 million bits that will be used in testing.


Testing the Data:
    To run the SP800-22 testing suite on files within generated above run tests.py with 1 command line argument:
        - path (string): The directory path of the directory to test. Example: "./test_data/my_data"

    This will produce a new directory within your specified directory containing the test results. Input file and result file will share the same name.