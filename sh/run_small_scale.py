import os
import sys
sys.path.append(".")
from utils import print_green
# run 5 times for each task in the Small_Scale
# python sh/test_small_1_MRT.py
# python sh/test_small_2_PTT.py
# python sh/test_small_3_WLT.py
# python sh/test_small_4_MPFB.py
# python sh/test_small_5_JLO.py

for i in range(5):
    print_green("Run {} times for each task in the Small_Scale".format(i+1))
    os.system("python sh/test_small_1_MRT.py")
    os.system("python sh/test_small_2_PTT.py")
    os.system("python sh/test_small_3_WLT.py")
    os.system("python sh/test_small_4_MPFB.py")
    os.system("python sh/test_small_5_JLO.py")
    