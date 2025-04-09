import os

def test_dir(dir):
    sum_zeros = 0
    sum_ones = 0
    try:
        for file in os.listdir(dir):
            with open(f"{dir}/{file}", "r") as f:
                path = os.path.join(dir, file)

                if(not os.path.isfile(path)):
                    continue
                d = f.read()

            zero = 0
            one = 0
            for i in range(len(d)):
                if(d[i] == "0"):
                    zero += 1 
                else:
                    one += 1

            sum_zeros += zero
            sum_ones += one

            return sum_zeros, sum_ones
    except:
        pass

dir = "./test_data/lcg_20"
zeros, ones = test_dir(dir)
print(f"{dir}: Zeros: {zeros}, Ones: {ones}")

dir = "./test_data/lsb_only"
zeros, ones = test_dir(dir)
print(f"{dir}: Zeros: {zeros}, Ones: {ones}")