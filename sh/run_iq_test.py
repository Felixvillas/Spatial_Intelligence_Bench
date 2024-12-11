import os
import sys
sys.path.append(".")
from utils import print_green
# run 5 times for each task in the IQ_Test
# python sh/test_iq_test.py

for i in range(5):
    print_green("Run {} times for each task in the IQ_Test".format(i+1))
    os.system("python sh/test_iq_test.py")
    