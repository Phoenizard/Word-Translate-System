# coding=utf-8
import argparse
import sys
import os
import requests
import uploadCurrentFrec as ucf
import CombineData as com

current_root = os.getcwd()
text_root = ""
result_root = ""
frequency_root = ""


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--text", type=str, default=None)  # txt(file name in source)
    arges = parser.parse_args()
    # python3 main.py --text=HarryPotter.txt
    name = arges.text
    text_root = current_root + "/source/" + name
    result_root = current_root + "/runs/" + name
    frequency_root = current_root + "/frec/frec_" + name
    src_root = current_root + "/data/wordlist-test.txt" # remember to change
    ucf.ucf(text_root, frequency_root)
    # Create txt frequency txt
    print("Update the database")
    com.combination(src_root, frequency_root)
    # Combine with the original one
    # combination(src, tmp)
